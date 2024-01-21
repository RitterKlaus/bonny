import unittest

from services.parser_dm import ParserDM

class TestParseDM(unittest.TestCase):
    def setUp(self):
        self.parserdm = ParserDM()

    def test_irgendwas(self):
        self.assertEqual(7, 7)

    def test_parse_receipt_number_1(self):
        gefunden, ergebnis = self.parserdm.parse_receipt_number('Beleg-Nr.      3456')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '3456')

    def test_parse_receipt_number_2(self):
        gefunden, ergebnis = self.parserdm.parse_receipt_number('  Beleg-Nr.      3456  ')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '3456')

    def test_parse_receipt_number_negative(self):
        gefunden, ergebnis = self.parserdm.parse_receipt_number('Schokolade     3456')
        self.assertFalse(gefunden)

    def test_parse_date_of_purchase_1(self):
        gefunden, ergebnis = self.parserdm.parse_date_of_purchase('Datum:     29.09.2023')
        self.assertTrue(gefunden)
        print(ergebnis)
        self.assertEqual(ergebnis, '29.09.2023')

    def test_parse_date_of_purchase_2(self):
        gefunden, ergebnis = self.parserdm.parse_date_of_purchase('Datum:     29.09.2023  ')
        self.assertTrue(gefunden)
        print(ergebnis)
        self.assertEqual(ergebnis, '29.09.2023')

if __name__ == '__main__':
    unittest.main()