from abc import ABC, abstractmethod
from datetime import datetime
import pytz

import bonny_config as bonny_config

class Parser(ABC):

    def __init__(self):
        self.market = 'abstract'
        self.TZ = pytz.timezone(bonny_config.TIMEZONE)

    def truncate_after_third_last_space(self, input_string):
        # Finden Sie die Position des drittletzten Leerzeichens
        third_last_space_position = input_string.rfind(' ', 0, input_string.rfind(' ', 0, input_string.rfind(' ')))

        if third_last_space_position != -1:
            # Schneiden Sie alles nach dem drittletzten Leerzeichen ab
            result_string = input_string[:third_last_space_position]
            return result_string
        else:
            return input_string  # Wenn weniger als drei Leerzeichen vorhanden sind
    
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
