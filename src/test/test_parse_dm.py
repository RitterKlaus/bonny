import unittest

from parse_dm import dm_parse_receipt_number, dm_parse_date_of_purchase

class TestDmParser(unittest.TestCase):
    def test_irgendwas(self):
        self.assertEqual(3, 33)

    def test_dm_parse_receipt_number_1(self):
        gefunden, ergebnis = dm_parse_receipt_number('Beleg-Nr.      3456')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '3456')

    def test_dm_parse_receipt_number_2(self):
        gefunden, ergebnis = dm_parse_receipt_number('  Beleg-Nr.      3456  ')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '3456')

    def test_dm_parse_receipt_number_negative(self):
        gefunden, ergebnis = dm_parse_receipt_number('Schokolade     3456')
        self.assertFalse(gefunden)

    def test_dm_parse_date_of_purchase_1(self):
        gefunden, ergebnis = dm_parse_date_of_purchase('Datum:     29.09.2023')
        self.assertTrue(gefunden)
        print(ergebnis)
        self.assertEqual(ergebnis, '29.09.2023')

    def test_dm_parse_date_of_purchase_2(self):
        gefunden, ergebnis = dm_parse_date_of_purchase('Datum:     29.09.2023  ')
        self.assertTrue(gefunden)
        print(ergebnis)
        self.assertEqual(ergebnis, '29.09.2023')

if __name__ == '__main__':
    unittest.main()