# sso.tax Contributing Guidelines

## Running Locally

Requires Ruby and Bundler. Install dependencies with:

```
bundle install
```

Then serve the site with:

```
bundle exec jekyll serve
```

## Call Us
Vendors whose `sso_pricing` field contains any of the words "call", "contact", "custom", or "quote" (case-insensitive) are automatically sorted into "The Other List" below "The List." Examples: `Call Us!`, `Contact Sales`, `Custom pricing`.

## Percentages
A common error with PRs is a miscalculated percentage. The site uses a "percentage increase from base price model" – that is, a $5 -> $10 markup is a 100% increase, not 200%. The script that checks PRs will check this math, or will insert the field itself if you don't provide it, as long as the units are consistent.

It's fiddly to get right first time, so here's the convenient formula:

(Higher Price - Lower Price) / Lower Price * 100

## Vendor Notes
If a vendor's pricing entry needs additional context (e.g. "SSO price only becomes visible after signing up to the Pro plan"), add a `vendor_note` field with a plain-text explanation:

```yaml
vendor_note: SSO price only becomes visible when you have already signed up to the Pro plan.
```

This will appear as an ⓘ icon next to the vendor name on the site. Clicking or hovering over it shows the note.

## Pricing Source Info
If pricing data comes from a non-public source such as a sales quote, add a `pricing_source_info` field:

```yaml
pricing_source_info: Pricing comes from a quote
```

This will appear as an ⓘ icon next to the pricing source link. Do not use the old `pricing_note` or `footnotes` fields — these are no longer supported.
