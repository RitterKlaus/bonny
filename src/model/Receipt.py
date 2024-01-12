import bonny_config as bonny_config
from peewee import *

db = SqliteDatabase(bonny_config.DATABASE)

class Receipt(Model):
    store = CharField()                   # Markt
    date_of_purchase = DateTimeField()    # Belegdatum
    number = CharField()                  # Belegnummer

    class Meta:
        database = db