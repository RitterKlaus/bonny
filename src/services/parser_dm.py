import re
from datetime import datetime

from model.Article import Article
from model.Receipt import Receipt
from services.parser import Parser

def truncate_after_third_last_space(input_string):
    # Finden Sie die Position des drittletzten Leerzeichens
    third_last_space_position = input_string.rfind(' ', 0, input_string.rfind(' ', 0, input_string.rfind(' ')))

    if third_last_space_position != -1:
        # Schneiden Sie alles nach dem drittletzten Leerzeichen ab
        result_string = input_string[:third_last_space_position]
        return result_string
    else:
        return input_string  # Wenn weniger als drei Leerzeichen vorhanden sind

class ParserDM(Parser):

    def __init__(self):
        self.market = 'dm'

    def parse_artikelzeile(self, zeile):
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

    def parse_receipt_number(self, zeile):
        pattern = r'Beleg-Nr\.\s*([0-9]+)'
        match = re.search(pattern, zeile)
        
        if match:
            beleg_nr = match.group(1)
            print("Beleg-Nr.:", beleg_nr)
            return True, beleg_nr
        else:
            return False, None
        
    def parse_date_of_purchase(self, zeile):
        pattern = re.compile(r"Datum:\s+(\d{2}\.\d{2}.\d{4})")
        match = re.search(pattern, zeile)
        
        if match:
            date_of_purchase = match.group(1)
            return True, date_of_purchase
        else:
            return False, None

    def extrahiere_daten(self, pdf):
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
            gefunden, betrag, mwst = self.parse_artikelzeile(text_content)
            if gefunden:
                artikelzeilen.append(truncate_after_third_last_space(text_content))
                print ('Betrag:', betrag, ' MwSt: ', mwst)
                article = Article(description = truncate_after_third_last_space(text_content),
                                price = betrag,
                                tax = 0,
                                store = storename,
                                date_of_purchase = datetime(2023, 10, 3,
                                                            15, 0, 0, 0,
                                                            tzinfo=self.TZ))
                article.save()
            dop_found, found_dop = self.parse_date_of_purchase(text_content)
            if dop_found:
                receipt.date_of_purchase = found_dop
            number_found, found_number = self.parse_receipt_number(text_content)
            if number_found:
                receipt.number = found_number
        receipt.save()
        print (artikelzeilen)
        return artikelzeilen 

