import re
from datetime import datetime

from model.Article import Article
from model.Receipt import Receipt
from services.parser import Parser

import pytz
import bonny_config as bonny_config

def truncate_after_third_last_space(input_string):
    # Finden Sie die Position des drittletzten Leerzeichens
    third_last_space_position = input_string.rfind(' ', 0, input_string.rfind(' ', 0, input_string.rfind(' ')))

    if third_last_space_position != -1:
        # Schneiden Sie alles nach dem drittletzten Leerzeichen ab
        result_string = input_string[:third_last_space_position]
        return result_string
    else:
        return input_string  # Wenn weniger als drei Leerzeichen vorhanden sind


class ParserREWE(Parser):

    def __init__(self):
        self.market = 'REWE'
        self.TZ = pytz.timezone(bonny_config.TIMEZONE)


    def parse_receipt_number(self, zeile):
        pattern = r'Beleg-Nr\.\s*([0-9]+)'
        match = re.search(pattern, zeile)
        
        if match:
            beleg_nr = match.group(1)
            print("Beleg-Nr.:", beleg_nr)
            return True, beleg_nr
        else:
            return False, None

    def parse_artikelzeile(self, zeile):
        """Eine Zeile mit Artikel bei REWE ist wie folgt aufgebaut:
        'JA! H-MILCH 1,5% 11,40 B '
        '<Artikelname> <Preis> <Mehrwertsteuersatz> '
        """

        pattern = r'(\d+,\d+)\s([AB])'
        match = re.search(pattern, zeile)
        
        if match:
            betrag_mwst = match.group(1)
            mwst = match.group(2)
            print('Betrag: ', betrag_mwst)
            return True, betrag_mwst, mwst
        else:
            return False, None, None

    def extract_article(self, text):
        pattern = r'^(.*?)\s+(\d+,\d+)\s+([A-Za-z])\s*$'
        match = re.match(pattern, text)
        if match:
            return match.group(1).strip()
        return None

    def parse_date_of_purchase(self, zeile):
        pattern = re.compile(r"Datum:\s+(\d{2}\.\d{2}.\d{4})")
        match = re.search(pattern, zeile)
        
        if match:
            date_of_purchase = match.group(1)
            return True, date_of_purchase
        else:
            return False, None
   
    def extrahiere_daten(self, pdf):
        """Der E-Bon von REWE ist zeilenweise aufgebaut.
        Diese Funktion liest alle Zeilen und verwirft alle, die keine Artikel-Zeilen sind.
        """

        receipt = Receipt(store = self.market, date_of_purchase = datetime.now(), number = 'none') # mit unbekannten Werten starten 
        
        # Definieren Sie den XPath-Ausdruck, um nach LTTextBoxHorizontal-Tags zu suchen
        xpath_expression = '//LTTextBoxHorizontal'

        # Extrahieren Sie die Texte aus den gefundenen Tags
        text_elements = pdf.tree.xpath(xpath_expression)
        for zeile in text_elements:
            for element in zeile:
                text_content = element.text
                print('Zu durchsuchende Zeile: ', text_content)

                gefunden, betrag, mwst = self.parse_artikelzeile(text_content)
                
                if gefunden:
                    print ('Betrag:', betrag, ' MwSt: ', mwst)
                    produktname = self.extract_article(text_content)
                    if produktname:
                        article = Article(description = produktname,
                                        price = betrag,
                                        tax = 0,
                                        store = self.market,
                                        date_of_purchase = datetime(2023, 10, 3,
                                                                    15, 0, 0, 0,
                                                                    tzinfo=self.TZ))
                        print('Zu speichernde Zeile: ', text_content)
                        print('Artikelbeschreibung: ', produktname)
                        article.save()

                dop_found, found_dop = self.parse_date_of_purchase(text_content)
                if dop_found:
                    receipt.date_of_purchase = found_dop
                
                number_found, found_number = self.parse_receipt_number(text_content)
                if number_found:
                    receipt.number = found_number

        receipt.save()
        return True 