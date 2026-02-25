# Contributing to sso.tax

## Quick start: adding a vendor

1. Create `_vendors/yourvendor.yaml` (lowercase, hyphens instead of spaces)
2. Copy the template below and fill it in
3. Open a PR — the validation bot will check your submission automatically

## Vendor YAML template

```yaml
---
name: Example Vendor
base_pricing: $10 per user/month
sso_pricing: $25 per user/month
percent_increase: 150%
vendor_url: https://example.com
pricing_source: https://example.com/pricing
updated_at: 2024-01-15
# Optional fields — include only if relevant:
# vendor_note: SSO requires the Enterprise plan, which bundles other features.
# pricing_source_info: Pricing comes from a quote
```

## Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Vendor's display name |
| `base_pricing` | Yes | Lowest reasonable business-tier price (not free/personal tiers) |
| `sso_pricing` | Yes | Cheapest tier that includes SSO. Use `Call Us!` if not publicly listed. |
| `percent_increase` | Yes* | `(sso - base) / base * 100`. The validator will tell you the correct value if you get it wrong. |
| `vendor_url` | Yes | Vendor's homepage URL |
| `pricing_source` | Yes | Direct link to the pricing page. Can be a list of URLs. Non-URL values (e.g. `Quote`) are accepted but discouraged. |
| `updated_at` | Yes | Date pricing was last verified, in `YYYY-MM-DD` format |
| `vendor_note` | No | Context shown as an info icon next to the vendor name (plain text) |
| `pricing_source_info` | No | Context shown as an info icon next to the source link (e.g. `Pricing comes from a quote`) |

\* If you omit `percent_increase` and both prices are parseable, the validator will calculate it for you and tell you what to add.

## Calculating the percentage

The site uses a "percentage increase from base price" model:

**(SSO price - Base price) / Base price * 100**

A $5 to $10 markup is a **100%** increase, not 50%. The validator checks this math and will flag mismatches.

Make sure `base_pricing` and `sso_pricing` use the same units (e.g. both "per user/month"). The bot will warn if the units don't match — it's not blocking, but mismatched units usually mean the percentage is comparing apples to oranges.

## "Call Us" vendors

If the vendor doesn't publish SSO pricing, set `sso_pricing` to something like `Call Us!`, `Contact Sales`, or `Custom pricing`. The site detects the keywords *call*, *contact*, *custom*, and *quote* (case-insensitive) and sorts these vendors into "The Other List" instead of the main table.

## Vendor notes and pricing source info

Use `vendor_note` when a vendor's pricing entry needs context that isn't obvious from the numbers alone:

```yaml
vendor_note: SSO requires the Enterprise plan, which bundles other features.
```

This appears as an info icon next to the vendor name on the site.

Use `pricing_source_info` when pricing data comes from a non-public source:

```yaml
pricing_source_info: Pricing comes from a quote
```

This appears as an info icon next to the pricing source link.

## What the validation bot does

When you open a PR that changes files in `_vendors/`, the bot automatically:

- **Checks schema**: required fields present, valid date format, valid URLs
- **Validates percentage math**: compares your `percent_increase` against the calculated value
- **Flags deprecated fields**: the old `footnotes` and `pricing_note` fields are no longer supported
- **Labels the PR**: with specific labels like `validation: passed`, `validation: schema error`, etc.

**Errors** must be fixed before merging. **Warnings** are flagged for maintainer review but won't block the PR.

## Running locally

This is optional — the validation bot and GitHub Pages preview will catch most issues.

Requires Ruby (version pinned in `.ruby-version`) and Bundler. Use a version manager like [mise](https://mise.jdx.dev/) or [rbenv](https://github.com/rbenv/rbenv) to pick up the correct version automatically:

```
mise install        # or: rbenv install
bundle install
bundle exec jekyll serve
```

To run the validator locally:

```
python3 scripts/validate_pricing.py _vendors/yourvendor.yaml
```
