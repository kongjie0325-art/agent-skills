# HTTPS Push with GitHub PAT — Quick Reference

## The Core Problem

GitHub disabled password authentication for Git operations (2021). Using a PAT over HTTPS requires a specific auth format, and the `git credential.helper store` approach has quirks.

## Authentication Methods Compared

| Method | Token exposed in `git remote -v`? | Reusable across repos? | Setup effort |
|--------|----------------------------------|----------------------|--------------|
| `https://x-access-token:TOKEN@github.com/...` | ✅ Yes (visible in .git/config) | ✅ Yes | Low |
| Custom credential helper script | ❌ No | ✅ Yes | Medium |
| `gh auth setup-git` | ❌ No | ✅ Yes | Low (needs `gh`) |
| SSH key auth | ❌ No | ✅ Yes | High |

## Method 1: Token in Remote URL (quick & dirty)

```bash
git remote set-url origin https://x-access-token:FULL_TOKEN@github.com/owner/repo.git
```

**Caveat:** Anyone who can run `git remote -v` sees the token. Don't use on shared machines.

## Method 2: Custom Credential Helper (recommended)

```bash
# One-time setup
cat > ~/.git-cred-helper.sh << 'EOF'
#!/bin/sh
echo "username=x-access-token"
echo "password=FULL_TOKEN_HERE"
EOF
chmod +x ~/.git-cred-helper.sh
git config --global credential.helper "!~/.git-cred-helper.sh"
```

After this, all `git push/pull/clone` over HTTPS works without any per-repo config.

## Method 3: gh CLI (if available)

```bash
echo "FULL_TOKEN" | gh auth login --with-token
gh auth setup-git
```

## Common Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| `fatal: Authentication failed` | Token truncated or wrong in credential helper | Verify full token string, re-save |
| `remote: Invalid username or password` | Using `x-oauth-basic` as password instead of token | Use the PAT itself as password, not `x-oauth-basic` |
| `403 on POST /user/repos` with `github_pat_` token | Fine-grained PATs can't create repos | Generate classic token (`ghp_` prefix) with `repo` scope |
| `Resource not accessible by personal access token` | Token lacks `repo` scope | Regenerate at https://github.com/settings/tokens |

## Token Type Cheat Sheet

- **Classic** (`ghp_XXXX...`): Can do anything the user can do, controlled by scope checkboxes. Use this.
- **Fine-grained** (`github_pat_...`): Per-repo permissions, cannot create repos, cannot use many REST endpoints. Avoid for automation.

## Extraction Patterns

```bash
# From git credential store
TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')

# From gh CLI
TOKEN=$(gh auth token 2>/dev/null)

# From .env file (Hermes)
TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
```
