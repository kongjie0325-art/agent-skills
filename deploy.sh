#!/bin/bash
# Agent Skills Hub — 一键部署脚本
# 将精选 Skills 部署到本地 Agent skills 目录

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="${SCRIPT_DIR}/skills"

# 检测 Agent 类型
detect_agent() {
    if [ -d "$HOME/.hermes/skills" ]; then
        echo "hermes"
    elif [ -d "$HOME/.claude/skills" ]; then
        echo "claude"
    elif [ -d "$HOME/.cursor/skills" ]; then
        echo "cursor"
    elif [ -d "$HOME/.openclaw/skills" ]; then
        echo "openclaw"
    else
        echo "unknown"
    fi
}

deploy_hermes() {
    local dest="$HOME/.hermes/skills"
    mkdir -p "$dest"
    echo "📦 Deploying to Hermes Agent: $dest"
    for skill_dir in "${SKILLS_SRC}"/*/; do
        local name=$(basename "$skill_dir")
        if [ -d "$skill_dir" ]; then
            cp -r "$skill_dir" "$dest/$name"
            echo "  ✅ Installed: $name"
        fi
    done
}

deploy_claude() {
    local dest="$HOME/.claude/skills"
    mkdir -p "$dest"
    echo "📦 Deploying to Claude Code: $dest"
    for skill_dir in "${SKILLS_SRC}"/*/; do
        local name=$(basename "$skill_dir")
        if [ -d "$skill_dir" ]; then
            cp -r "$skill_dir" "$dest/$name"
            echo "  ✅ Installed: $name"
        fi
    done
}

deploy_generic() {
    local dest="${1:-$HOME/.agent/skills}"
    mkdir -p "$dest"
    echo "📦 Deploying to: $dest"
    for skill_dir in "${SKILLS_SRC}"/*/; do
        local name=$(basename "$skill_dir")
        if [ -d "$skill_dir" ]; then
            cp -r "$skill_dir" "$dest/$name"
            echo "  ✅ Installed: $name"
        fi
    done
}

echo "🧠 Agent Skills Hub — Deploy"
echo "================================"

# 列出可用 Skills
echo ""
echo "📋 Available Skills:"
for skill_dir in "${SKILLS_SRC}"/*/; do
    local name=$(basename "$skill_dir")
    local desc=""
    if [ -f "$skill_dir/SKILL.md" ]; then
        desc=$(head -5 "$skill_dir/SKILL.md" | grep -E "^(#|description)" | head -1 | sed 's/^#\s*//' | cut -c1-60)
    fi
    echo "  • $name — $desc"
done
echo ""

# 检测并部署
AGENT=$(detect_agent)
echo "🔍 Detected Agent: $AGENT"
echo ""

case "$AGENT" in
    hermes)
        deploy_hermes
        ;;
    claude)
        deploy_claude
        ;;
    *)
        echo "⚠️  Unknown Agent. Deploying to ~/.agent/skills/"
        deploy_generic "$HOME/.agent/skills"
        ;;
esac

echo ""
echo "✅ Done! Skills deployed."
echo ""
echo "📊 三层能力模型:"
echo "  Skills (大脑经验) → 已部署 ✅"
echo "  MCP   (手和脚)   → https://github.com/kongjie0325-art/agent-mcp"
echo "  Plugin (特殊工具) → https://github.com/kongjie0325-art/agent-plugins"
