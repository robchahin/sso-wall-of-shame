"""
One-time migration script: replace footnotes and pricing_note fields.

- `footnotes: '[^id]: text'` → `vendor_note: text`
  Strips [^id] references from sso_pricing, base_pricing, percent_increase.
- `pricing_note: Quote` → `pricing_source_info: Pricing comes from a quote`
  Empty pricing_note fields are removed.

Run from the repo root:
  python3 scripts/migrate_footnotes.py
"""

import os
import re

VENDORS_DIR = os.path.join(os.path.dirname(__file__), '..', '_vendors')

# Matches a footnote definition prefix like "[^some-id]: "
FOOTNOTE_DEF_RE = re.compile(r'^\[\^[^\]]+\]:\s*')

# Matches any footnote reference like "[^some-id]"
FOOTNOTE_REF_RE = re.compile(r'\[\^[^\]]+\]')


def migrate_file(path):
    with open(path, 'r') as f:
        original = f.read()

    lines = original.splitlines(keepends=True)
    new_lines = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]

        # --- footnotes field ---
        if re.match(r'^footnotes:\s*', line):
            # Collect the full value (may be multi-line YAML block scalar)
            raw_value_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j] and lines[j][0] in (' ', '\t'):
                raw_value_lines.append(lines[j])
                j += 1

            # Extract the value portion from first line
            first = re.sub(r'^footnotes:\s*', '', raw_value_lines[0]).rstrip('\n')

            # Join continuation lines with a space (preserving word boundaries)
            rest_parts = [l.strip() for l in raw_value_lines[1:]]
            combined = (first + ' ' + ' '.join(rest_parts)).strip()

            # Remove surrounding single or double quotes
            if len(combined) >= 2 and combined[0] == combined[-1] and combined[0] in ('"', "'"):
                combined = combined[1:-1]

            # Handle YAML escaped single quotes ('') → (')
            combined = combined.replace("''", "'")

            # Strip the "[^id]: " prefix to get the note text
            note_text = FOOTNOTE_DEF_RE.sub('', combined).strip()

            if note_text:
                # Quote the value if it contains characters that would break plain YAML
                if "'" in note_text or ':' in note_text or '#' in note_text:
                    escaped = note_text.replace('"', '\\"')
                    new_lines.append(f'vendor_note: "{escaped}"\n')
                else:
                    new_lines.append(f'vendor_note: {note_text}\n')

            # Always mark changed so the file is rewritten (old field is dropped either way)
            changed = True
            i = j
            continue

        # --- pricing_note field ---
        if re.match(r'^pricing_note:\s*', line):
            value = re.sub(r'^pricing_note:\s*', '', line).strip()
            if value:
                if value.lower() == 'quote':
                    new_lines.append('pricing_source_info: Pricing comes from a quote\n')
                else:
                    new_lines.append(f'pricing_source_info: {value}\n')
            # Drop the field (renamed or empty); always mark changed
            changed = True
            i += 1
            continue

        # --- pricing fields: strip [^ref] references ---
        if re.match(r'^(sso_pricing|base_pricing|percent_increase):\s*', line):
            new_line, n = FOOTNOTE_REF_RE.subn('', line)
            if n > 0:
                new_lines.append(new_line)
                changed = True
            else:
                new_lines.append(line)
            i += 1
            continue

        new_lines.append(line)
        i += 1

    if changed:
        with open(path, 'w') as f:
            f.writelines(new_lines)
        return True
    return False


def main():
    vendors_dir = os.path.abspath(VENDORS_DIR)
    files = sorted(f for f in os.listdir(vendors_dir) if f.endswith(('.yaml', '.yml')))

    migrated = 0
    for filename in files:
        path = os.path.join(vendors_dir, filename)
        if migrate_file(path):
            print(f'  migrated: {filename}')
            migrated += 1

    print(f'\nDone. {migrated}/{len(files)} files updated.')


if __name__ == '__main__':
    main()
