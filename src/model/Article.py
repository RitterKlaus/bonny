import bonny_config as bonny_config
from peewee import *

db = SqliteDatabase(bonny_config.DATABASE)

class Article(Model):
    description = CharField()
    price = IntegerField()             # gespeichert als Cents
    tax = IntegerField()               # Mehrwertsteuersatz
    date_of_purchase = DateTimeField() # Kaufdatum
    store = CharField()                # Markt

    class Meta:
        database = db