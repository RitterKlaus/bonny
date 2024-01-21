from abc import ABC, abstractmethod
from datetime import datetime
import pytz

import bonny_config as bonny_config

class Parser(ABC):

    def __init__(self):
        self.market = 'abstract'
        self.TZ = pytz.timezone(bonny_config.TIMEZONE)

    @abstractmethod
    def parse_receipt_number():
        raise NotImplementedError

    @abstractmethod
    def parse_artikelzeile():
        raise NotImplementedError

    @abstractmethod
    def parse_date_of_purchase():
        raise NotImplementedError
    
    @abstractmethod
    def extrahiere_daten():
        raise NotImplementedError
