# 框架能力矩阵 — Claude Code vs Codex vs Cline vs Roo Code vs OpenHands

## 目录
- [一、总览矩阵](#一总览矩阵)
- [二、Skills 支持对比](#二skills-支持对比)
- [三、MCP 支持对比](#三mcp-支持对比)
- [四、Plugin 支持对比](#四plugin-支持对比)
- [五、Memory 对比](#五memory-对比)
- [六、Hooks/安全 对比](#六hooks安全-对比)
- [七、子代理对比](#七子代理对比)

---

## 一、总览矩阵

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **公司** | Anthropic | OpenAI | Anysphere | Roo Code Inc | OpenHands |
| **Stars** | 50K+ | 15K+ | 58.6K | 22.5K | 8K+ |
| **License** | Proprietary | Apache-2.0 | Apache-2.0 | Apache-2.0 | Apache-2.0 |
| **语言** | CLI + VS Code + JetBrains | CLI + IDE | VS Code 扩展 | VS Code 扩展 | CLI + IDE |
| **模型** | Claude 系列 | GPT 系列 | 多模型 | 多模型 | 多模型 |
| **Skills** | ★★★★★ | ★★★★ | ★★★ | ★★ | ★★ |
| **MCP** | ★★★★★ | ★★★ | ★★★ | ★★ | ★★★ |
| **Plugin** | ★★★★★ | ★★★ | ★ | ★ | ★★ |
| **Memory** | ★★★★★ | ★★★★ | ★★★ | ★★ | ★★★ |
| **Hooks** | ★★★★★ | ★★ | ★★ | ★★ | ★★★ |
| **子代理** | ★★★★★ | ★★★★ | ★★★ | ★★ | ★★★★ |
| **安全模型** | 应用层 Hooks | 内核层 Seatbelt | 应用层 | 应用层 | 沙箱 |

---

## 二、Skills 支持对比

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **格式** | SKILL.md | SKILL.md | SKILL.md | 自定义 | 自定义 |
| **标准** | 自有 → 开放 | 开放标准 | 兼容 SKILL.md | 部分兼容 | 部分兼容 |
| **安装** | `/plugin` + marketplace | `$skill-installer` | `.cline/skills/` | `.roo/` | 手动 |
| **Progressive Disclosure** | ✅ 三层加载 | ✅ | ✅ | ❌ | ❌ |
| **自动触发** | ✅ description 匹配 | ✅ | ✅ | 部分 | 部分 |
| **手动触发** | ✅ `/skill-name` | ✅ `$skill` | ✅ `/skill` | ✅ | ✅ |
| **脚本执行** | ✅ bash 沙箱 | ✅ | ✅ | 部分 | ✅ |
| **官方 Skills** | pptx/xlsx/docx/pdf | openai/skills 仓库 | 无 | 无 | 无 |
| **社区生态** | 400K+ 安装 | 快速增长 | 中等 | 小 | 小 |

### 关键发现

**SKILL.md 已成为事实标准**：
- Anthropic 发布 → OpenAI 采纳 → Cursor/Gemini/Copilot 跟进
- 40.9K+ stars 的 Superpowers 完全基于 SKILL.md
- 16.1K+ stars 的 Agent Skills for Context Engineering 全面覆盖

---

## 三、MCP 支持对比

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **MCP 深度** | 最深 | 中 | 中 | 浅 | 中 |
| **配置方式** | `.mcp.json` + 命令行 | 配置文件 | 自动发现 | 手动 | 配置文件 |
| **Deferred Tool Loading** | ✅ | ✅ (ToolSearch) | ❌ | ❌ | 部分 |
| **stdio 传输** | ✅ | ✅ | ✅ | 部分 | ✅ |
| **Streamable HTTP** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **OAuth 2.1** | ✅ | ✅ | 部分 | ❌ | 部分 |
| **MCP Apps (UI)** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **内置 MCP Servers** | 20+ | 10+ | 5+ | 2+ | 5+ |

### Claude Code 的 MCP 优势
- **Deferred Tool Loading (2026)**: 启动时只加载工具名，按需获取完整 schema
- 50+ 工具时减少 ~10% token 开销
- 远程 MCP Server 支持 OAuth 2.1 + PKCE

---

## 四、Plugin 支持对比

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **Plugin 市场** | ✅ `/plugin marketplace` | ✅ (UI) | ❌ | ❌ | ❌ |
| **Plugin 格式** | `plugin.json` | 无标准 | 无 | 无 | 自定义 |
| **打包内容** | Skills+Agents+Hooks+MCP | Skills+MCP | 无 | 无 | Skills+工具 |
| **安装方式** | 命令 + 市场 | UI + 手动 | - | - | 手动 |
| **分享方式** | Git/GitHub | GitHub | - | - | Git |

---

## 五、Memory 对比

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **项目记忆** | CLAUDE.md | AGENTS.md | .cursorrules | .roo/rules | 自定义 |
| **用户记忆** | ~/.claude/CLAUDE.md | AGENTS.md | 全局设置 | 全局设置 | 全局设置 |
| **层级** | 5 层级联 | 3 层 | 2 层 | 1 层 | 2 层 |
| **向量搜索** | ✅ | ✅ | ❌ | ❌ | 部分 |
| **RAG** | ✅ (Files API) | ✅ (file_search) | ❌ | ❌ | 部分 |
| **跨会话记忆** | ✅ | ✅ | 部分 | ❌ | ✅ |

### CLAUDE.md vs AGENTS.md

| 维度 | CLAUDE.md (Anthropic) | AGENTS.md (Linux Foundation) |
|------|----------------------|------------------------------|
| **维护方** | Anthropic | Linux Foundation AAIF |
| **采纳** | Claude Code 专有 | Codex/Cursor/Copilot/Gemini 共同 |
| **开放度** | 开放格式 | 开放标准 |
| **趋势** | 可能共存 | 可能成为统一标准 |

---

## 六、Hooks/安全 对比

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **Hook 数量** | 26 个事件 | 无 | 少量 | 少量 | 有 |
| **安全模型** | 应用层 Hooks | 内核层 Seatbelt/Landlock | 应用层 | 应用层 | 沙箱 |
| **可编程性** | 高（任意脚本）| 低（二进制开关）| 中 | 低 | 中 |
| **权限粒度** | per-tool 正则 | 3 种模式 | per-tool | 全局 | per-tool |
| **审批策略** | 3 级 | 3 级 | 2 级 | 1 级 | 2 级 |
| **逃逸阻力** | 中 | 高 | 中 | 低 | 高 |

---

## 七、子代理对比

| 维度 | Claude Code | OpenAI Codex | Cline | Roo Code | OpenHands |
|------|-------------|--------------|-------|----------|-----------|
| **子代理** | ✅ 内置 | ✅ Handoffs | ✅ | ✅ | ✅ |
| **Agent Teams** | ✅ 实验性 | ✅ Handoffs | ❌ | ❌ | ✅ |
| **内置子代理** | Explore/Plan/General | 无 | 无 | 无 | 多个 |
| **自定义子代理** | ✅ AGENTS.md | ✅ | 部分 | ❌ | ✅ |
| **隔离上下文** | ✅ fork | ✅ | 部分 | 部分 | ✅ |
| **并行执行** | ✅ | ✅ | ✅ | 部分 | ✅ |

---

**下一节 →** [../frameworks/claude-code.md](../frameworks/claude-code.md) — Claude Code 完整架构分析
