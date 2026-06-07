# GitHub Token Scope Reference

## Quick Detection

When a PAT returns 200 on GET /user but 403 on write operations (POST /user/repos, push),
the token is valid but lacks the required scope. This is the most common PAT misconfiguration.

### One-liner to check scopes
```bash
curl -s -I -H "Authorization: token $TOKEN" https://api.github.com/user | grep -i x-oauth-scopes
```

### One-liner to test write access
```bash
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"name":"_scope_test","auto_init":false}' \
  https://api.github.com/user/repos
# 201 = has scope, 403 = missing scope
```

## Common Scope Gaps

| Missing Scope | Symptom | Fix |
|---|---|---|
| `repo` | 403 on POST /user/repos, push, PR creation | Regenerate PAT with `repo` checked |
| `workflow` | 403 on .github/workflows modifications | Add `workflow` scope |
| `write:packages` | 403 on package publish | Add `write:packages` scope |
| `admin:org` | 403 on org-level operations | Add `admin:org` scope |

## PAT vs Fine-grained Token

- **Classic PAT**: Scopes are broad (`repo` = full repo access). Check at https://github.com/settings/tokens
- **Fine-grained PAT**: Repository-specific, no broad scopes. Cannot use `repo` scope. These tokens **cannot create repos** by design — the user must create the repo manually or use a classic PAT.

If the user's token is a fine-grained PAT and the task requires repo creation, tell them to either:
1. Create a **classic PAT** with `repo` scope at https://github.com/settings/tokens/new
2. Manually create the repo and provide the URL for the agent to push to
