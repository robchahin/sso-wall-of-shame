import os
import re
import yaml
import argparse
import sys
from datetime import datetime

REQUIRED_FIELDS = ['name', 'base_pricing', 'sso_pricing', 'vendor_url', 'pricing_source', 'updated_at']

KNOWN_FIELDS = {
    'name', 'base_pricing', 'sso_pricing', 'percent_increase',
    'vendor_url', 'pricing_source', 'updated_at', 'vendor_note', 'pricing_source_info',
    # Deprecated fields — kept here to suppress the generic "unknown field" warning;
    # a specific deprecation warning is issued instead (see validate_schema).
    'footnotes', 'pricing_note',
}

DEPRECATED_FIELDS = {
    'footnotes': (
        "The 'footnotes' field is deprecated. "
        "Use 'vendor_note' with plain text instead. "
        "See CONTRIBUTING.md for details."
    ),
    'pricing_note': (
        "The 'pricing_note' field is deprecated. "
        "Use 'pricing_source_info' with plain text instead (e.g. 'Pricing comes from a quote'). "
        "See CONTRIBUTING.md for details."
    ),
}

class _DuplicateKeyLoader(yaml.SafeLoader):
    """SafeLoader that raises an error on duplicate YAML keys."""
    def construct_mapping(self, node, deep=False):
        keys = [self.construct_object(key_node, deep=deep) for key_node, _ in node.value]
        duplicates = {k for k in keys if keys.count(k) > 1}
        if duplicates:
            raise yaml.YAMLError(f"Duplicate key(s) in YAML: {', '.join(sorted(duplicates))}")
        return super().construct_mapping(node, deep=deep)


def extract_price(price_str):
    """
    Extracts the first valid monetary amount from a string.
    Returns a float if found, otherwise returns None.
    """
    if not isinstance(price_str, str):
        price_str = str(price_str)

    # Remove commas that might be used as thousand separators
    clean_str = price_str.replace(',', '')

    # Match the first sequence of digits and optional decimals
    match = re.search(r'(\d+(?:\.\d+)?)', clean_str)
    if match:
        return float(match.group(1))
    return None

def extract_unit(price_str):
    """
    Extracts the unit suffix from a pricing string by stripping the leading
    currency symbol(s) and numeric value. Returns a normalised lowercase string,
    or empty string if nothing remains (e.g. bare '$10').

    Examples:
      '$10 per u/m'  -> 'per u/m'
      '4.99€ / device' -> '€ / device'  (currency attached to number, kept)
      '$2,500'       -> ''
    """
    if not isinstance(price_str, str):
        price_str = str(price_str)
    clean_str = price_str.replace(',', '')
    # Strip leading currency symbols before the number
    clean_str = re.sub(r'^[\$€£¥]+', '', clean_str).strip()
    # Remove the first number (including decimals)
    unit = re.sub(r'^\d+(?:\.\d+)?', '', clean_str).strip()
    return unit.lower()

def is_call_us(pricing_str):
    """
    Heuristic to determine if pricing implies "Call Us" / Custom.
    """
    if not isinstance(pricing_str, str):
        return False
    lower_str = pricing_str.lower()
    return any(keyword in lower_str for keyword in ['call', 'custom', 'quote', 'contact'])

def _is_valid_url(value):
    """Returns True if value looks like a valid http/https URL."""
    return isinstance(value, str) and re.match(r'https?://', value) is not None

def validate_schema(data, warnings, errors):
    """
    Validates required fields, known fields, date format, and URL format.
    Mutates warnings and errors in place.
    """
    # Required fields
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            errors.append(f"Missing required field: '{field}'.")

    # Unknown fields (typo detection)
    unknown = set(data.keys()) - KNOWN_FIELDS
    if unknown:
        warnings.append(f"Unknown field(s): {', '.join(sorted(unknown))}. Check for typos.")

    # Deprecated fields
    for field, message in DEPRECATED_FIELDS.items():
        if field in data:
            warnings.append(message)

    # updated_at must be a parseable date
    updated_at = data.get('updated_at')
    if updated_at:
        try:
            datetime.strptime(str(updated_at), '%Y-%m-%d')
        except ValueError:
            errors.append(f"'updated_at' value '{updated_at}' is not a valid YYYY-MM-DD date.")

    # vendor_url must look like a URL
    vendor_url = data.get('vendor_url')
    if vendor_url and not _is_valid_url(vendor_url):
        errors.append(f"'vendor_url' does not look like a valid URL: '{vendor_url}'.")

    # pricing_source can be a string or list; each entry must look like a URL
    pricing_source = data.get('pricing_source')
    if pricing_source:
        sources = pricing_source if isinstance(pricing_source, list) else [pricing_source]
        for src in sources:
            if not _is_valid_url(src):
                errors.append(f"'pricing_source' entry does not look like a valid URL: '{src}'.")


def validate_vendor_file(filepath):
    """
    Validates a single vendor YAML file.
    Returns (is_valid, warnings, errors)
    """
    warnings = []
    errors = []

    try:
        with open(filepath, 'r') as f:
            content = f.read()
        # Use duplicate-key-detecting loader
        data = yaml.load(content, Loader=_DuplicateKeyLoader)
    except yaml.YAMLError as e:
        errors.append(f"Failed to parse YAML: {e}")
        return False, warnings, errors
    except Exception as e:
        errors.append(f"Failed to read file: {e}")
        return False, warnings, errors

    if not data:
        errors.append("Empty YAML file.")
        return False, warnings, errors

    # Schema validation
    validate_schema(data, warnings, errors)

    # Strip legacy footnote references (e.g. "[^id]") from pricing fields so
    # old-format PRs don't generate spurious percentage warnings on top of the
    # deprecation warning already issued above.
    footnote_ref = re.compile(r'\[\^[^\]]+\]')
    base_pricing = footnote_ref.sub('', str(data.get('base_pricing') or '')).strip() or None
    sso_pricing = footnote_ref.sub('', str(data.get('sso_pricing') or '')).strip() or None
    percent_increase_raw = data.get('percent_increase')

    if not base_pricing or not sso_pricing:
        # Already caught by schema validation; no need to go further
        return len(errors) == 0, warnings, errors

    # Parse provided user percentage
    provided_pct = None
    if isinstance(percent_increase_raw, (int, float)):
        provided_pct = float(percent_increase_raw)
    elif isinstance(percent_increase_raw, str):
        # Remove '%' and parse
        pct_clean = percent_increase_raw.replace('%', '').strip()
        try:
            provided_pct = float(pct_clean)
        except ValueError:
            pass # e.g. "???" or "N/A"

    # Check for "Call Us" exceptions
    if is_call_us(sso_pricing):
        # We don't strictly calculate. We just check if the user provided a number which would be weird.
        if provided_pct is not None:
            warnings.append(f"SSO pricing looks like 'Contact Us' ('{sso_pricing}'), but a numeric percentage ({provided_pct}%) was provided.")
        return len(errors) == 0, warnings, errors

    # Extract numeric values
    base_val = extract_price(base_pricing)
    sso_val = extract_price(sso_pricing)

    if base_val is None or sso_val is None:
        warnings.append(f"Could not extract numeric price from base ('{base_pricing}') and/or sso ('{sso_pricing}'). Manual review recommended.")
        return len(errors) == 0, warnings, errors

    # Warn if the unit suffixes differ — the percentage is still calculated and
    # checked below (likely a typo), but if units mismatch the percentage check
    # is also downgraded to a warning since the numbers may not be comparable.
    base_unit = extract_unit(base_pricing)
    sso_unit = extract_unit(sso_pricing)
    units_match = base_unit == sso_unit
    if not units_match:
        warnings.append(
            f"Pricing units appear to differ: base='{base_pricing}', sso='{sso_pricing}'. "
            f"Please verify the percentage is calculated on a like-for-like basis."
        )

    if base_val == 0:
        warnings.append("Base pricing is $0. Cannot calculate percentage increase.")
        return len(errors) == 0, warnings, errors

    # Calculate percentage
    calculated_pct = ((sso_val - base_val) / base_val) * 100

    # If the user didn't provide a parseable percentage but we calculated one.
    # Downgrade to a warning if units differ, since the calculated value may not be meaningful.
    if provided_pct is None:
        formatted_pct = f"{calculated_pct:.0f}"
        msg = (
            f"Missing 'percent_increase'. "
            f"Based on base=${base_val} and sso=${sso_val}, "
            f"the value should be: percent_increase: {formatted_pct}%"
        )
        if units_match:
            errors.append(msg)
            return False, warnings, errors
        else:
            warnings.append(msg)
            return len(errors) == 0, warnings, errors

    # Compare
    # Allow a small margin of error for rounding (e.g., 200% instead of 199.9%)
    margin = 1.5 # 1.5% margin allows for 33% instead of 33.3% rounding by users
    if abs(calculated_pct - provided_pct) > margin:
        msg = (
            f"Percentage mismatch: expected {calculated_pct:.1f}%, "
            f"got {provided_pct}%. "
            f"Prices: base=${base_val}, sso=${sso_val}."
        )
        if units_match:
            errors.append(msg)
        else:
            warnings.append(msg)

    return len(errors) == 0, warnings, errors

def main():
    parser = argparse.ArgumentParser(description="Validate SSO Wall of Shame vendor pricing.")
    parser.add_argument("paths", nargs='+', help="Vendor YAML files or directories containing them.")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Exit with error code if there are warnings.")
    args = parser.parse_args()

    filepaths_to_check = []
    for path in args.paths:
        if os.path.isfile(path) and path.endswith(('.yml', '.yaml')):
            filepaths_to_check.append(path)
        elif os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(('.yml', '.yaml')):
                    filepaths_to_check.append(os.path.join(path, filename))
        else:
            print(f"Skipping invalid path: {path}")

    # Collect all results first so we can emit category markers at the end
    results = {}
    for filepath in filepaths_to_check:
        is_valid, warnings, errors = validate_vendor_file(filepath)
        results[filepath] = (errors, warnings)

    # Print per-file output
    for filepath, (errors, warnings) in results.items():
        filename = os.path.basename(filepath)
        if errors:
            print(f"❌ {filename}")
            for error in errors:
                print(f"   Error: {error}")
        if warnings:
            print(f"⚠️ {filename}")
            for warning in warnings:
                print(f"   Warning: {warning}")

    # Emit machine-readable category markers for the workflow to map to PR labels.
    # These are derived from error messages using stable keyword matches — never
    # from free-text that could be influenced by PR content.
    categories = set()
    for errors, _ in results.values():
        for e in errors:
            if any(k in e for k in ["Missing required field", "not a valid", "Unknown field", "Duplicate", "Empty YAML", "Failed to parse", "Failed to read"]):
                categories.add("CATEGORY:schema-error")
            if any(k in e for k in ["percent_increase", "Percentage mismatch"]):
                categories.add("CATEGORY:pricing-error")
    for cat in sorted(categories):
        print(cat)

    files_with_errors = sum(1 for e, _ in results.values() if e)
    files_with_warnings = sum(1 for _, w in results.values() if w)
    total_files = len(results)

    print("\n" + "="*40)
    print(f"Validation complete. Scanned {total_files} files.")
    print(f"Errors: {files_with_errors} files")
    print(f"Warnings: {files_with_warnings} files")

    if files_with_errors > 0:
        sys.exit(1)

    if args.fail_on_warnings and files_with_warnings > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
