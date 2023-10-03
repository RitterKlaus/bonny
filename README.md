# bonny
Tool, um e-Bons zu extrahieren und Daten über das eigene Kaufverhalten zu sammeln.
Das Skript durchsucht das Verzeichnis /input nach PDF-Dateien und schreibt eine CSV-Dateien 
Aktuell werden unterstützt:
* dm drogerie-markt

In Planung:
* REWE

# Vorbereitung zu Entwicklung

pip install pdfquery
pip install pandas
pip install peewee

# Hilfreiche Doku

* https://docs.peewee-orm.com/en/latest/peewee/quickstart.html
* CSV-Trennzeichen als kwargs mitgeben https://stackoverflow.com/questions/16823695/how-to-use-delimiter-for-csv-in-python
* CSV-Leerzeilen vermeiden https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row