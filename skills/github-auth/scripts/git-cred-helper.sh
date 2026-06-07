#!/bin/sh
# Git credential helper — returns a GitHub PAT for HTTPS operations.
#
# Usage:
#   1. Replace YOUR_TOKEN_HERE with your actual GitHub PAT
#   2. Save as ~/.git-cred-helper.sh and chmod +x
#   3. git config --global credential.helper "!~/.git-cred-helper.sh"
#
# This avoids embedding the token in remote URLs (visible via `git remote -v`)
# and works across all repos without per-repo config.
#
# IMPORTANT: Use the FULL token, not a truncated copy from chat context.

echo "username=x-access-token"
echo "password=YOUR_TOKEN_HERE"
