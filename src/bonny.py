import pdfquery
import os

from peewee import SqliteDatabase
from playhouse.dataset import DataSet

import pytz

import bonny_config as bonny_config
import parse_dm as parse_dm
from services.parser_rewe import ParserREWE
from model.Article import Article
from model.Receipt import Receipt

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
    
    Aktuell wird nur dm drogerie-markt und REWE erkannt."""

    supermarkt = None
    daten = pdf.extract([
        ('with_formatter', 'text'),
        ('supermarkt_rewe', ':contains("REWE Markt GmbH")', lambda match: 'REWE' if match else ''),
        ('supermarkt_dm', ':contains("ffnungszeiten auf dm.de")', lambda match: 'dm' if match else ''),
    ])

    # Überprüfe, welcher Supermarkt gefunden wurde
    if daten['supermarkt_dm'] == 'dm':
        supermarkt = 'dm'
    elif daten['supermarkt_rewe'] == 'REWE':
        supermarkt = 'REWE'
    else:
        supermarkt = None
    return supermarkt


def main():
    # Wechsle in das Verzeichnis des Scripts als Arbeitsverzeichnis
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pfad = os.getcwd() + '/../input'
    pdf_liste = liste_pdf_in_verzeichnis(pfad)

    for pdf_datei in pdf_liste:
        # PDF lesen und Inhalt in XML konvertieren
        pdf = pdfquery.PDFQuery(pdf_datei)
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
            print('Extrahiere Daten aus dem E-Bon ', pdf_datei, ' von: dm-drogerie markt.')
            #parse_dm.extrahiere_von_dm(pdf)
        elif supermarkt == 'REWE':
            print('Extrahiere Daten aus dem E-Bon ', pdf_datei, ' von: REWE.')
            rewe_parser = ParserREWE()
            rewe_parser.extrahiere_daten(pdf)
        else:
            print('Das E-Bon-Format von ', pdf_datei, ' ist mir leider nicht bekannt.')
        db.close()

        # Datenbank als CSV exportieren
        ds = DataSet('sqlite:///' + bonny_config.DATABASE)
        query = Article.select().order_by(Article.id)
        # delimiter und lineterminator werden von peewee/playhouse an die Bibliothek CSVExporter weitergereicht
        ds.freeze(query = query, format='csv', filename='../output/bonny_export.csv', encoding='utf8', delimiter=';', lineterminator='\n')
        ds.close()


if __name__ == "__main__":
    main()
