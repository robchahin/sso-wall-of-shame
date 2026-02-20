import unittest
import sys
import os

# Add parent directory to path to import script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.validate_pricing import extract_price, is_call_us

class TestValidatePricing(unittest.TestCase):

    def test_extract_price_standard(self):
        self.assertEqual(extract_price("$23.99"), 23.99)
        self.assertEqual(extract_price("$10 per u/m"), 10.0)
        self.assertEqual(extract_price("$2,500[^price-note]"), 2500.0)
        
    def test_extract_price_euro(self):
        self.assertEqual(extract_price("€10 per u/m"), 10.0)
        self.assertEqual(extract_price("4.99€ / device"), 4.99)
        
    def test_extract_price_no_price(self):
        self.assertIsNone(extract_price("???"))
        self.assertIsNone(extract_price("Call Us!"))
        
    def test_is_call_us(self):
        self.assertTrue(is_call_us("Call Us!"))
        self.assertTrue(is_call_us("Contact Sales"))
        self.assertTrue(is_call_us("Custom Quote"))
        self.assertTrue(is_call_us("Request a quote"))
        self.assertFalse(is_call_us("$10 per user"))

if __name__ == '__main__':
    unittest.main()
