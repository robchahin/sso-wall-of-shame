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
