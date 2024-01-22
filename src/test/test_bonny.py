import unittest
import pdfquery

import bonny

class TestBonny(unittest.TestCase):

    def test_erkenne_supermarkt_dm(self):
         pdf = pdfquery.PDFQuery('./input/dm-eBon_2023-09-26_18-50-13.pdf.pdf')
         supermarkt = bonny.erkenne_supermarkt(pdf)
         self.assertEqual(supermarkt, 'dm')

    def test_erkenne_supermarkt_rewe(self):
         pdf = pdfquery.PDFQuery('./input/REWE-eBon.pdf')
         supermarkt = bonny.erkenne_supermarkt(pdf)
         self.assertEqual(supermarkt, 'REWE')