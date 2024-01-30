import re
from datetime import datetime

from model.Article import Article
from model.Receipt import Receipt
from services.parser import Parser

class ParserREWE(Parser):

    def __init__(self):
        self.market = 'REWE'

    def parse_receipt_number(self, text_content):
        return '1'


    def parse_artikelzeile(self, zeile):
        """Eine Zeile mit Artikel bei REWE ist wie folgt aufgebaut:
        'JA! H-MILCH 1,5% 11,40 B '
        '<Artikelname> <Preis> <Mehrwertsteuersatz> '
        """

        pattern = r'\w+\s*(\d+\,\d+)\s([AB])\s'
        match = re.search(pattern, zeile)
        
        if match:
            betrag_mwst = match.group(1)
            mwst = match.group(2)
            print('Betrag: ', betrag_mwst)
            return True, betrag_mwst, mwst
        else:
            return False, None, None


    def parse_date_of_purchase(self, text_content):
        return '12-12-1212'
   
    def extrahiere_daten(self, pdf):
        """Der E-Bon von REWE ist zeilenweise aufgebaut.
        Diese Funktion liest alle Zeilen und verwirft alle, die keine Artikel-Zeilen sind.
        """
        receipt = Receipt(store = self.market, date_of_purchase = datetime.now(), number = 'none') # mit unbekannten Werten starten
        # Extrahieren Sie die Texte aus den gefundenen Tags
        text_elements = pdf.tree.xpath('//LTTextLineHorizontal')
        artikelzeilen = []
        for element in text_elements:
            text_content = element.text      
            print (text_content)    
        return artikelzeilen 