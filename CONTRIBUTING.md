# sso.tax Contributing Guidelines

## Running Locally

Requires Ruby 3.2+ and Bundler. Install dependencies with:

```
bundle install
```

Then serve the site with:

```
bin/serve
```

This wrapper script handles Ruby 4.0+ compatibility (methods removed from stdlib). Do not use `bundle exec jekyll serve` directly — it will fail on Ruby 4.0+.
## Call Us
Vendors with the word "Call" in the sso_pricing field are automatically sorted into "The Other List" below "The List."

## Percentages
A common error with PRs is a miscalculated percentage. The site uses a "percentage increase from base price model" – that is, a $5 -> $10 markup is a 100% increase, not 200%. I'm hoping that a unit test will catch these, but writing a guideline is quicker.

It's fiddly to get right first time, so here's the convenient formula:

(Higher Price - Lower Price) / Lower Price * 100
