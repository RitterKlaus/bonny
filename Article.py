import BonnyConfig
from peewee import *

db = SqliteDatabase(BonnyConfig.DATABASE)

class Article(Model):
    description = CharField()
    price = IntegerField()             # gespeichert als Cents
    tax = IntegerField()               # Mehrwertsteuersatz
    date_of_purchase = DateTimeField() # Kaufdatum
    store = CharField()                # Markt

    class Meta:
        database = db