import unittest
import sys
import os
import tempfile

# Add parent directory to path to import script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.validate_pricing import extract_price, is_call_us, validate_schema, validate_vendor_file

class TestExtractPrice(unittest.TestCase):

    def test_extract_price_standard(self):
        self.assertEqual(extract_price("$23.99"), 23.99)
        self.assertEqual(extract_price("$10 per u/m"), 10.0)
        self.assertEqual(extract_price("$2,500"), 2500.0)

    def test_extract_price_euro(self):
        self.assertEqual(extract_price("€10 per u/m"), 10.0)
        self.assertEqual(extract_price("4.99€ / device"), 4.99)

    def test_extract_price_no_price(self):
        self.assertIsNone(extract_price("???"))
        self.assertIsNone(extract_price("Call Us!"))


class TestIsCallUs(unittest.TestCase):

    def test_call_us_variants(self):
        self.assertTrue(is_call_us("Call Us!"))
        self.assertTrue(is_call_us("Contact Sales"))
        self.assertTrue(is_call_us("Custom Quote"))
        self.assertTrue(is_call_us("Request a quote"))

    def test_not_call_us(self):
        self.assertFalse(is_call_us("$10 per user"))


class TestValidateSchema(unittest.TestCase):

    def _make_valid_data(self):
        return {
            'name': 'Test Vendor',
            'base_pricing': '$10 per u/m',
            'sso_pricing': '$20 per u/m',
            'vendor_url': 'https://example.com',
            'pricing_source': 'https://example.com/pricing',
            'updated_at': '2024-01-15',
        }

    def test_valid_data_no_errors(self):
        warnings, errors = [], []
        validate_schema(self._make_valid_data(), warnings, errors)
        self.assertEqual(errors, [])

    def test_missing_required_field(self):
        data = self._make_valid_data()
        del data['vendor_url']
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("vendor_url" in e for e in errors))

    def test_invalid_date_format(self):
        data = self._make_valid_data()
        data['updated_at'] = '15-01-2024'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("updated_at" in e for e in errors))

    def test_invalid_vendor_url(self):
        data = self._make_valid_data()
        data['vendor_url'] = 'example.com'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("vendor_url" in e for e in errors))

    def test_invalid_pricing_source_url(self):
        data = self._make_valid_data()
        data['pricing_source'] = 'not-a-url'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("pricing_source" in e for e in errors))

    def test_pricing_source_list(self):
        data = self._make_valid_data()
        data['pricing_source'] = ['https://example.com/a', 'https://example.com/b']
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertEqual(errors, [])

    def test_unknown_field_warns(self):
        data = self._make_valid_data()
        data['vender_url'] = 'https://typo.example.com'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("vender_url" in w for w in warnings))

    def test_vendor_note_is_known_field(self):
        data = self._make_valid_data()
        data['vendor_note'] = 'SSO requires an enterprise plan.'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertEqual(errors, [])
        self.assertFalse(any("vendor_note" in w for w in warnings))

    def test_pricing_source_info_is_known_field(self):
        data = self._make_valid_data()
        data['pricing_source_info'] = 'Pricing comes from a quote'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertEqual(errors, [])
        self.assertFalse(any("pricing_source_info" in w for w in warnings))

    def test_old_footnotes_field_warns_deprecated(self):
        data = self._make_valid_data()
        data['footnotes'] = '[^foo]: some note'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("deprecated" in w.lower() and "vendor_note" in w for w in warnings))
        # Must not also fire the generic unknown-field warning
        self.assertFalse(any("Unknown field" in w and "footnotes" in w for w in warnings))

    def test_old_pricing_note_field_warns_deprecated(self):
        data = self._make_valid_data()
        data['pricing_note'] = 'Quote'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        self.assertTrue(any("deprecated" in w.lower() and "pricing_source_info" in w for w in warnings))
        # Must not also fire the generic unknown-field warning
        self.assertFalse(any("Unknown field" in w and "pricing_note" in w for w in warnings))

    def test_footnote_refs_stripped_before_percentage_check(self):
        # A PR using the old footnotes style should not get a spurious percentage warning
        data = self._make_valid_data()
        data['sso_pricing'] = '$20 per u/m[^foo]'
        data['footnotes'] = '[^foo]: some note'
        data['percent_increase'] = '100%'
        warnings, errors = [], []
        validate_schema(data, warnings, errors)
        # Deprecation warning yes, percentage mismatch warning no
        self.assertTrue(any("deprecated" in w.lower() for w in warnings))
        self.assertFalse(any("Percentage mismatch" in w for w in warnings))


class TestDuplicateKeys(unittest.TestCase):

    def test_duplicate_key_raises_error(self):
        yaml_content = "name: Foo\nbase_pricing: $5\nname: Bar\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            tmpfile = f.name
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertFalse(is_valid)
            self.assertTrue(any("Duplicate" in e for e in errors))
        finally:
            os.unlink(tmpfile)


if __name__ == '__main__':
    unittest.main()
