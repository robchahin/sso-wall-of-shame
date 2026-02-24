import unittest
import sys
import os
import tempfile

# Add parent directory to path to import script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.validate_pricing import extract_price, extract_unit, is_call_us, validate_schema, validate_vendor_file

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
        self.assertEqual(errors, [])
        self.assertTrue(any("pricing_source" in w for w in warnings))

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


class TestPercentIncrease(unittest.TestCase):

    def _write_tempfile(self, content):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        f.write(content)
        f.close()
        return f.name

    def _valid_yaml(self, extra=''):
        return (
            "name: Test\n"
            "base_pricing: $10 per u/m\n"
            "sso_pricing: $20 per u/m\n"
            "vendor_url: https://example.com\n"
            "pricing_source: https://example.com/pricing\n"
            "updated_at: 2024-01-15\n"
            + extra
        )

    def test_missing_percent_increase_is_error(self):
        tmpfile = self._write_tempfile(self._valid_yaml())
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertFalse(is_valid)
            self.assertTrue(any("percent_increase" in e for e in errors))
            self.assertTrue(any("100%" in e for e in errors))
        finally:
            os.unlink(tmpfile)

    def test_missing_percent_increase_does_not_modify_file(self):
        tmpfile = self._write_tempfile(self._valid_yaml())
        try:
            original = open(tmpfile).read()
            validate_vendor_file(tmpfile)
            self.assertEqual(open(tmpfile).read(), original)
        finally:
            os.unlink(tmpfile)

    def test_wrong_percent_increase_is_error(self):
        tmpfile = self._write_tempfile(self._valid_yaml("percent_increase: 50%\n"))
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertFalse(is_valid)
            self.assertTrue(any("mismatch" in e.lower() for e in errors))
        finally:
            os.unlink(tmpfile)

    def test_correct_percent_increase_passes(self):
        tmpfile = self._write_tempfile(self._valid_yaml("percent_increase: 100%\n"))
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertTrue(is_valid)
            self.assertEqual(errors, [])
        finally:
            os.unlink(tmpfile)


class TestExtractUnit(unittest.TestCase):

    def test_per_user_month(self):
        self.assertEqual(extract_unit("$10 per u/m"), "per u/m")

    def test_bare_number(self):
        self.assertEqual(extract_unit("$2,500"), "")

    def test_currency_after_number(self):
        # e.g. '4.99€ / device' — leading $ strip doesn't apply, number is stripped
        self.assertEqual(extract_unit("4.99€ / device"), "€ / device")

    def test_per_month(self):
        self.assertEqual(extract_unit("$100 per month"), "per month")

    def test_per_year(self):
        self.assertEqual(extract_unit("$995 per year"), "per year")


class TestUnitMismatch(unittest.TestCase):

    def _write_tempfile(self, content):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        f.write(content)
        f.close()
        return f.name

    def _yaml(self, base, sso, pct=None):
        content = (
            "name: Test\n"
            f"base_pricing: {base}\n"
            f"sso_pricing: {sso}\n"
            "vendor_url: https://example.com\n"
            "pricing_source: https://example.com/pricing\n"
            "updated_at: 2024-01-15\n"
        )
        if pct:
            content += f"percent_increase: {pct}\n"
        return content

    def test_unit_mismatch_emits_warning(self):
        tmpfile = self._write_tempfile(self._yaml("$10 per u/m", "$20 per month", "100%"))
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertTrue(any("units appear to differ" in w for w in warnings))
        finally:
            os.unlink(tmpfile)

    def test_unit_mismatch_downgrades_pct_error_to_warning(self):
        # Wrong percentage but units differ — should warn, not error
        tmpfile = self._write_tempfile(self._yaml("$10 per u/m", "$20 per month", "50%"))
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertEqual(errors, [])
            self.assertTrue(any("mismatch" in w.lower() for w in warnings))
        finally:
            os.unlink(tmpfile)

    def test_unit_mismatch_downgrades_missing_pct_to_warning(self):
        # Missing percent_increase but units differ — should warn, not error
        tmpfile = self._write_tempfile(self._yaml("$10 per u/m", "$20 per month"))
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertEqual(errors, [])
            self.assertTrue(any("percent_increase" in w for w in warnings))
        finally:
            os.unlink(tmpfile)

    def test_matching_units_keeps_pct_as_error(self):
        # Same units, wrong percentage — must still be an error
        tmpfile = self._write_tempfile(self._yaml("$10 per u/m", "$20 per u/m", "50%"))
        try:
            is_valid, warnings, errors = validate_vendor_file(tmpfile)
            self.assertFalse(is_valid)
            self.assertTrue(any("mismatch" in e.lower() for e in errors))
        finally:
            os.unlink(tmpfile)


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
