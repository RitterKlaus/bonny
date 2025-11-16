import unittest

from services.parser_rewe import ParserREWE

class TestParseREWE(unittest.TestCase):
    def setUp(self):
        self.parserrewe = ParserREWE()

    def test_irgendwas(self):
        self.assertEqual(7, 7)

    def test_parse_receipt_number_1(self):
        gefunden, ergebnis = self.parserrewe.parse_receipt_number('Beleg-Nr. 9334')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '9334')

    def test_parse_receipt_number_2(self):
        gefunden, ergebnis = self.parserrewe.parse_receipt_number('  Beleg-Nr.      3456  ')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '3456')

    def test_parse_receipt_number_negative(self):
        gefunden, ergebnis = self.parserrewe.parse_receipt_number('Schokolade     3456')
        self.assertFalse(gefunden)

    def test_parse_date_of_purchase_1(self):
        gefunden, ergebnis = self.parserrewe.parse_date_of_purchase('Datum:     29.09.2023')
        self.assertTrue(gefunden)
        print(ergebnis)
        self.assertEqual(ergebnis, '29.09.2023')

    def test_parse_date_of_purchase_2(self):
        gefunden, ergebnis = self.parserrewe.parse_date_of_purchase('Datum:     29.09.2023  ')
        self.assertTrue(gefunden)
        print(ergebnis)
        self.assertEqual(ergebnis, '29.09.2023')

    def test_parse_artikelzeile_1(self):
        gefunden, betrag, mwst = self.parserrewe.parse_artikelzeile('JA! H-MILCH 1,5% 11,40 B ')
        self.assertTrue(gefunden)
        self.assertEqual(betrag, '11,40')
        self.assertEqual(mwst, 'B')

    def test_parse_artikelzeile_2(self):
        gefunden, betrag, mwst = self.parserrewe.parse_artikelzeile('RADIESCHEN 0,65 B')
        self.assertTrue(gefunden)
        self.assertEqual(betrag, '0,65')
        self.assertEqual(mwst, 'B')

    def test_parse_artikelzeile_3(self):
        gefunden, betrag, mwst = self.parserrewe.parse_artikelzeile('KUECHENTUECHER 2,75 A')
        self.assertTrue(gefunden)
        self.assertEqual(betrag, '2,75')
        self.assertEqual(mwst, 'A')

    def test_parse_artikel1(self):
        artikelname = self.parserrewe.extract_article('KUECHENTUECHER 2,75 A')
        self.assertEqual(artikelname, 'KUECHENTUECHER')

    def test_parse_artikel2(self):
        artikelname = self.parserrewe.extract_article('JA! H-MILCH 1,5% 11,40 B ')
        self.assertEqual(artikelname, 'JA! H-MILCH 1,5%')

    def test_parse_artikel3(self):
        artikelname = self.parserrewe.extract_article('HER FIN HAEHN BR 2,49 B ')
        self.assertEqual(artikelname, 'HER FIN HAEHN BR')

    def test_parse_artikel4(self):
        artikelname = self.parserrewe.extract_article('SCHINKEN M. PF 2,49 B')
        self.assertEqual(artikelname, 'SCHINKEN M. PF')

if __name__ == '__main__':
    unittest.main()