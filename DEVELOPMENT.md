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

- Ruby 3.4.8 (pinned in `.ruby-version`, managed via `mise`)
- Python 3 with PyYAML if testing GitHub Actions scripts
- `bundle exec jekyll serve` to preview locally
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

### Limitations of workflow_dispatch

`workflow_dispatch` **cannot** retroactively simulate a `pull_request` event. When validate-vendors.yml runs on a PR, it has access to PR context: changed files (via `tj-actions/changed-files`), the PR number for commenting, and the head branch for auto-commits. None of this context exists when triggered via `workflow_dispatch`.

This means you **cannot** use `workflow_dispatch` to run the vendor validation workflow against an old PR that predated the workflow. To validate old PRs, you'd need to either:
- Re-push the branch (triggers the workflow as a new PR event)
- Or build dedicated `workflow_dispatch` inputs that accept a PR number and reconstruct the context (not yet implemented)

For workflows that don't depend on PR context (scheduled jobs like the dead link checker), `workflow_dispatch` works identically to the real trigger.

## Branch Naming

- `fix/` — bug fixes
- `feat/` — new features
