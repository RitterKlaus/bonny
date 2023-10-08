import pdfquery
import os
import re

from peewee import SqliteDatabase
from playhouse.dataset import DataSet

from datetime import datetime
import pytz

import src.bonny_config as bonny_config
from src.model.Article import Article
from src.model.Receipt import Receipt

TZ = pytz.timezone(bonny_config.TIMEZONE)


def liste_pdf_in_verzeichnis(pfad):
    """Listet alle PDF-Dateien in einem Verzeichnis auf."""
    pdf_dateien = []

    # Überprüfe, ob das Verzeichnis existiert
    if not os.path.exists(pfad):
        print(f"Das Verzeichnis {pfad} existiert nicht.")
        return pdf_dateien

    # Durchsuche das Verzeichnis nach Dateien
    for dateiname in os.listdir(pfad):
        dateipfad = os.path.join(pfad, dateiname)

        # Überprüfe, ob es sich um eine Datei handelt und ob die Datei eine PDF-Datei ist
        if os.path.isfile(dateipfad) and dateipfad.lower().endswith('.pdf'):
            pdf_dateien.append(dateipfad)

    return pdf_dateien


def erkenne_supermarkt(pdf):
    """Erkenne den Supermarkt anhand von eindeutigen Merkmalen im E-Bon.
    
    Aktuell wird nur dm drogerie-markt erkannt."""

    daten = pdf.extract([
        ('supermarkt', ':contains("ffnungszeiten auf dm.de")', lambda match: match.text()[-5:-3])
    ])
    return daten["supermarkt"] # idealerweise 'dm', wenn es sich um dm handelt


def truncate_after_third_last_space(input_string):
    # Finden Sie die Position des drittletzten Leerzeichens
    third_last_space_position = input_string.rfind(' ', 0, input_string.rfind(' ', 0, input_string.rfind(' ')))

    if third_last_space_position != -1:
        # Schneiden Sie alles nach dem drittletzten Leerzeichen ab
        result_string = input_string[:third_last_space_position]
        return result_string
    else:
        return input_string  # Wenn weniger als drei Leerzeichen vorhanden sind


def dm_parse_artikelzeile(zeile):
    """Eine Zeile bei dm ist wie folgt aufgebaut:
    'dmBio Aufstrich Paprika+Hanf 1,99 2 '
    '<Artikelname> <Preis> <Mehrwertsteuersatz> '
    """

    pattern = r'\w+\s*(\d+\,\d+)\s([12])\s'
    match = re.search(pattern, zeile)
    
    if match:
        betrag_mwst = match.group(1)
        mwst = match.group(2)
        return True, betrag_mwst, mwst
    else:
        return False, None, None

def dm_parse_receipt_number(zeile):
    pattern = r'Beleg-Nr\.\s*([0-9]+)'
    match = re.search(pattern, zeile)
    
    if match:
        beleg_nr = match.group(1)
        print("Beleg-Nr.:", beleg_nr)
        return True, beleg_nr
    else:
        return False, None
    
def dm_parse_date_of_purchase(zeile):
    pattern = r'\w+\s*(\d+\,\d+)\s([12])\s'
    match = re.search(pattern, zeile)
    
    if match:
        betrag_mwst = match.group(1)
        mwst = match.group(2)
        return True, betrag_mwst
    else:
        return False, None

def extrahiere_von_dm(pdf):
    """Der E-Bon von dm-drogerie markt ist zeilenweise aufgebaut.
    Diese Funktion liest alle Zeilen und verwirft alle, die keine Artikel-Zeilen sind.
    """

    storename = 'dm'
    # Definieren Sie den XPath-Ausdruck, um nach LTTextBoxHorizontal-Tags zu suchen
    xpath_expression = '//LTTextBoxHorizontal'

    receipt = Receipt(store = storename, date_of_purchase = datetime.now(), number = 'none') # mit unbekannten Werten starten
    # Extrahieren Sie die Texte aus den gefundenen Tags
    text_elements = pdf.tree.xpath(xpath_expression)
    artikelzeilen = []
    for element in text_elements:
        text_content = element.text
        gefunden, betrag, mwst = dm_parse_artikelzeile(text_content)
        if gefunden:
            artikelzeilen.append(truncate_after_third_last_space(text_content))
            print ('Betrag:', betrag, ' MwSt: ', mwst)
            article = Article(description = truncate_after_third_last_space(text_content),
                              price = betrag,
                              tax = 0,
                              store = storename,
                              date_of_purchase = datetime(2023, 10, 3,
                                                          15, 0, 0, 0,
                                                          tzinfo=TZ))
            article.save()
        dop_found, found_dop = dm_parse_date_of_purchase(text_content)
        if dop_found:
            receipt.date_of_purchase = found_dop
        number_found, found_number = dm_parse_receipt_number(text_content)
        if number_found:
            receipt.number = found_number
    receipt.save()
    print (artikelzeilen)
    return artikelzeilen 


def main():
    # Wechsle in das Verzeichnis des Scripts als Arbeitsverzeichnis
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pfad = os.getcwd() + '/../input'
    pdf_liste = liste_pdf_in_verzeichnis(pfad)

    for pdf in pdf_liste:
        # PDF lesen und Inhalt in XML konvertieren
        pdf = pdfquery.PDFQuery(pdf)
        pdf.load()
        pdf.tree.write('../tmp/ebon.xml', pretty_print = True, encoding='utf-8')

        # Datenbank öffnen
        db = SqliteDatabase(bonny_config.DATABASE)
        db.connect()
        db.create_tables([Article, Receipt])

        # Format des E-Bons erkennen
        supermarkt = erkenne_supermarkt(pdf)

        # Abhängig vom erkannten Supermarkt E-Bon lesen
        if supermarkt == 'dm':
            print('Extrahiere Daten aus dem E-Bon von: dm-drogerie markt.')
            extrahiere_von_dm(pdf)
        else:
            print('Das E-Bon-Format ist mir leider nicht bekannt.')
        db.close()

        # Datenbank als CSV exportieren
        ds = DataSet('sqlite:///' + bonny_config.DATABASE)
        query = Article.select().order_by(Article.id)
        # delimiter und lineterminator werden von peewee/playhouse an die Bibliothek CSVExporter weitergereicht
        ds.freeze(query = query, format='csv', filename='../output/bonny_export.csv', encoding='utf8', delimiter=';', lineterminator='\n')
        ds.close()


if __name__ == "__main__":
    main()
