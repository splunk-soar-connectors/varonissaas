# How to Skip Pre-Commit Locally

## Quick Answer

Use the `--no-verify` (or `-n`) flag when committing:

```bash
git commit --no-verify -m "Your commit message"
```

Or the short form:

```bash
git commit -n -m "Your commit message"
```

## Common Scenarios

### 1. Skip Pre-Commit for One Commit
```bash
git commit --no-verify -m "fix: update regex wheels"
```

### 2. Skip Pre-Commit and Push
```bash
git commit --no-verify -m "Your message"
git push
```

### 3. Amend Last Commit Without Pre-Commit
```bash
git commit --amend --no-verify --no-edit
```

## Skip Specific Pre-Commit Hooks

If you want to run pre-commit but skip certain hooks, use the `SKIP` environment variable:

```bash
# Skip one hook
SKIP=package-app-dependencies git commit -m "Your message"

# Skip multiple hooks (comma-separated)
SKIP=package-app-dependencies,semgrep git commit -m "Your message"

# Skip slow hooks
SKIP=package-app-dependencies,semgrep,detect-secrets git commit -m "Your message"
```

## For Your Current Situation

Since you have all the wheel changes ready, you can commit with:

```bash
cd /mnt/k/src/splunk-soar-connectors

# Add everything
git add -A

# Commit without running pre-commit (fastest)
git commit --no-verify -m "fix: update regex wheels to 2025.11.3 and resolve formatting

- Update regex dependency from 2024.11.6 to 2025.11.3
- Add new regex wheels for Python 3.9 and 3.13
- Remove old wheel files
- Fix markdown formatting and whitespace issues
- Add allowlist pragma for example API key"

# Push to your PR
git push
```

## Why Skip Pre-Commit?

Valid reasons:
- ✅ Pre-commit hooks are slow (package-app-dependencies takes 5+ minutes)
- ✅ You've already run the checks manually
- ✅ CI will run the checks anyway
- ✅ You're fixing issues that pre-commit already identified

**Note**: The GitHub Actions CI will still run all pre-commit checks, so any issues will be caught there.

## Alternative: Disable Pre-Commit Temporarily

```bash
# Uninstall pre-commit hooks
pre-commit uninstall

# Make commits (no pre-commit will run)
git commit -m "Your message"

# Re-install when needed
pre-commit install
```

## Your Commit Command (Ready to Use)

```bash
git commit --no-verify -m "fix: update regex wheels to 2025.11.3 and resolve pre-commit issues"
git push
```

This will bypass all local pre-commit hooks and push directly to your PR!

