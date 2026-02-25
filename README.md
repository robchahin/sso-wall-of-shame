# sso.tax

A community-maintained list of vendors that charge extra for SSO (single sign-on). The live site is at **[sso.tax](https://sso.tax)**.

## How it works

Each vendor is a YAML file in `_vendors/`. Jekyll builds the site and deploys to GitHub Pages on every push to main. Vendors are sorted into two tables: **The List** (vendors with published SSO pricing, sorted by markup percentage) and **The Other List** (vendors that require contacting sales).

## Contributing

Know a vendor that charges extra for SSO? Add a YAML file and open a PR — a validation bot will check your submission automatically. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide and YAML template.

## For maintainers

See [DEVELOPMENT.md](DEVELOPMENT.md) for repo architecture, testing workflows, and branch conventions.

## License

Apache 2.0 — see [LICENSE](LICENSE).
