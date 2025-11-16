# bonny
Tool, um e-Bons zu extrahieren und Daten über das eigene Kaufverhalten zu sammeln.
Das Skript durchsucht das Verzeichnis /input nach PDF-Dateien und schreibt eine CSV-Datein

Aktuell werden unterstützt:

* dm drogerie-markt

# Noch in Arbeit

* REWE (erkennt schon Artikel, aber noch kein Quittungsdatum
* Speichern des Datums eines Kaufs (Extrahieren aus dem E-Bon)
* Speichern des korrekten Kaufpreises
* Speichern des Mehwertsteuersatzes

# Voraussetzungen

* Python 3.13

# Installation

1. Virtuelle Umgebung anlegen: `python -m venv path/to/working/folder/.venv`
2. Virtuelle Umgebung aktivieren: `.venv/Scripts/Activate`
3. Abhängigkeiten installieren: `pip install -r requirements.txt`
4. Quittungen von REWE oder dm in das Verzeichnis /input kopieren
5. Das Skript src/bonny.py ausführen
6. Im Verzeichnis /output befindet sich nun eine CSV-Datei mit allen einzelnen auf den Quittungen gelisteten Artikeln.

# Hilfreiche Doku

* https://docs.peewee-orm.com/en/latest/peewee/quickstart.html
* CSV-Trennzeichen als kwargs mitgeben https://stackoverflow.com/questions/16823695/how-to-use-delimiter-for-csv-in-python
* CSV-Leerzeilen vermeiden https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
* https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure/24266885#24266885