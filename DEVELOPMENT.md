# Development Guide

## Repo Architecture

**Primary repo:** `robchahin/sso-wall-of-shame` (public, GitHub Pages)

All development happens here. Feature branches, PRs, and merges all target this repo directly. Use **squash-and-merge** for PRs to keep main history clean.

**Scratchpad repo:** `robchahin/sso-integ` (private)

Exists only for testing GitHub Actions workflows that have noisy side effects (opening issues, posting PR comments, auto-committing). Not a development environment. Not kept in sync — force-push from prod when you need a fresh copy:

```bash
git fetch origin
git push sso-integ origin/main:main --force
```

## Local Development

- Ruby 3.4.8 (pinned in `.ruby-version`). Use [mise](https://mise.jdx.dev/) or [rbenv](https://github.com/rbenv/rbenv) to pick up the pinned version automatically — your system Ruby will almost certainly be wrong.
- Python 3 with PyYAML for the validation script and tests
- `bundle install && bundle exec jekyll serve` to preview locally
- `vendor/` (used by Bundler) and `venv/` (used by tests) are in both `.gitignore` and `_config.yml` exclude list

## Testing GitHub Actions

### On feature branches (preferred)

Workflows with a `workflow_dispatch` trigger can be tested on any branch via the CLI, even if the workflow doesn't exist on main yet:

```bash
gh workflow run validate-vendors.yml --ref feat/my-feature
gh workflow run check-links.yml --ref feat/dead-link-checker
```

This is the primary way to test workflow changes before merging.

### On sso-integ (for noisy side effects)

If a workflow test will open issues, post comments, or otherwise create visible artifacts, test on sso-integ instead to keep the public repo clean:

```bash
# Sync sso-integ with current prod state
git push sso-integ origin/main:main --force

# Push your workflow branch
git push sso-integ feat/my-workflow:feat/my-workflow

# Trigger from sso-integ
gh workflow run check-links.yml --repo robchahin/sso-integ --ref feat/my-workflow
```

### Using workflow_dispatch for PR validation

The validate-vendors workflow has a `workflow_dispatch` trigger that accepts a PR number. This lets you retroactively validate any open PR:

```bash
gh workflow run validate-vendors.yml -f pr_number=123
```

The workflow fetches the PR's head SHA from the GitHub API, overlays `_vendors/` from that commit, runs validation, posts a comment, and updates labels — identical to an auto-triggered run. Very old PRs that predate the current YAML schema will produce deprecation warnings rather than useful validation output.

For workflows that don't depend on PR context (scheduled jobs like the dead link checker), `workflow_dispatch` works identically to the real trigger.

## Branch Naming

- `fix/` — bug fixes
- `feat/` — new features
