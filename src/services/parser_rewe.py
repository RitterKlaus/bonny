import re
from datetime import datetime

from model.Article import Article
from model.Receipt import Receipt
from services.parser import Parser

class ParserREWE(Parser):

    def __init__(self):
        self.market = 'REWE'

    def parse_receipt_number():
        raise NotImplementedError

    def parse_artikelzeile():
        raise NotImplementedError

    def parse_date_of_purchase():
        raise NotImplementedError
    
    def extrahiere_daten():
        raise NotImplementedError