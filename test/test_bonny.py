import unittest

from src.bonny import dm_parse_receipt_number

class TestBonny(unittest.TestCase):
    def test_irgendwas(self):
        self.assertEqual(3, 3)

    def test_dm_parse_receipt_number(self):
        gefunden, ergebnis = dm_parse_receipt_number('Beleg-Nr.      3456')
        self.assertTrue(gefunden)
        self.assertEqual(ergebnis, '3456')

    def test_dm_parse_receipt_number_negative(self):
        gefunden, ergebnis = dm_parse_receipt_number('Schokolade     3456')
        self.assertFalse(gefunden)

if __name__ == '__main__':
    unittest.main()