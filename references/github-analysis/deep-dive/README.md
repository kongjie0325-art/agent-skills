# Agent Skills × MCP × Plugin 辨析 + GitHub 全景检索

> 2026-07-07 | 基于 GitHub 全网检索，43+ 个仓库逐内容检查

## 📖 目录

- [一、核心定位](#一核心定位一句话区分)
- [二、Skills 深度解析](#二skills--agent-的大脑经验)
- [三、MCP 深度解析](#三mcp--agent-的手和脚)
- [四、Plugins 深度解析](#四plugins--agent-的工具包)
- [五、四者横向对比](#五四者横向对比含-subagents)
- [六、GitHub 仓库完整分类](#六github-仓库完整分类)
- [七、主流 Agent 框架内部架构对比](#七主流-agent-框架内部架构对比)
- [八、什么时候该用哪个](#八什么时候该用哪个)
- [九、最优组合](#九最优组合)
- [十、2026 年趋势](#十2026-年趋势)
- [参考资料](#参考资料)

---

## 一、核心定位：一句话区分

| 能力 | 本质 | 解决的问题 | 类比 | 格式 |
|------|------|-----------|------|------|
| **Skills** | 知识 + 流程模板 + 最佳实践 | 告诉 Agent **怎么做** | 🧠 大脑经验 | `SKILL.md`（Markdown） |
| **MCP** | 工具调用标准协议 | 让 Agent **能做** | 🤲 手和脚 | JSON-RPC 2.0 协议 |
| **Plugin** | 封装好的功能扩展包 | **增加**某个特定能力 | 🧰 专业工具 | `plugin.json` + 打包 |
| **Subagent** | 独立的专用 Agent 实例 | **隔离**特定任务 | 👷 专业工人 | `.agent.md` / YAML |

### 没有会怎样？

- **没有 Skills**：Agent 知道要部署，但不知道最佳流程 → 像实习生
- **没有 MCP**：Agent 知道流程，但无法操作 GitHub → 只能纸上谈兵
- **没有 Plugin**：Agent 能操作 GitHub，但无法调用某个特殊服务 → 能力有缺口
- **没有 Subagent**：所有任务都在主 context 里跑 → context 爆炸

---

## 二、Skills — Agent 的大脑经验

### 2.1 本质

```
Skill = Prompt + Workflow + Best Practice + 经验
```

### 2.2 Skills 标准：跨平台发现路径

| 工具 | 仓库级路径 | 用户级路径 | 全局路径 |
|------|-----------|-----------|---------|
| **Claude Code** | `.github/skills/` | `.claude/skills/` | `~/.claude/skills/` |
| **Codex CLI** | `.agents/skills/` | - | `~/.agents/skills/` |
| **Gemini CLI** | `.gemini/skills/` | - | `~/.gemini/skills/` |
| **GitHub Copilot** | `.github/skills/` | - | `~/.copilot/skills/` |
| **Cursor** | `.cursorrules` | - | `~/.cursor/rules/` |
| **OpenClaw** | `skills/` | - | `~/.openclaw/skills/` |

> **关键**：SKILL.md 格式在所有平台完全一致——写一次，到处可用。

### 2.3 核心优势

| 优势 | 说明 |
|------|------|
| 🧠 **提升推理质量** | 有 Skill 像高级工程师，没 Skill 像实习生 |
| 💰 **成本极低** | 30-50 tokens/Skill，按需加载 |
| 🔄 **极易迁移** | SKILL.md 格式通用，GPT/Claude/Gemini/GLM/Codex 全可用 |
| 🔍 **渐进式披露** | 只在相关时才加载完整内容，不占用 context |

### 2.4 核心局限

| 局限 | 说明 |
|------|------|
| ❌ **不能执行** | 只会说"应该这样做"，不会"真的去做" |
| ⏰ **容易过时** | K8s 2024 教程，2026 可能就过期了 |
| ⚠️ **Prompt 污染** | Skill 太多会冲突、覆盖、遗忘 |

---

## 三、MCP — Agent 的手和脚

### 3.1 本质

```
MCP = Model Context Protocol = 工具调用标准协议（JSON-RPC 2.0）
```

### 3.2 架构

```
┌─────────────┐     stdio/HTTP      ┌─────────────┐
│   Agent     │ ◄──────────────────► │  MCP Server │
│  (Client)   │    JSON-RPC 2.0     │  (Tool)     │
└─────────────┘                      └─────────────┘
```

### 3.3 核心优势

| 优势 | 说明 |
|------|------|
| 🔌 **通用标准** | 一次开发，全 Agent 使用 |
| 🛠️ **工具丰富** | 14,000+ 公共 Server |
| 🔄 **自主闭环** | 计划→执行→验证→修复→闭环 |
| 🏢 **企业级** | HTTP 传输支持 OAuth、RBAC、审计日志 |

### 3.4 核心局限

| 局限 | 说明 |
|------|------|
| 📦 **需要部署** | Node/Python/Docker 经常需要 |
| 🔐 **权限管理复杂** | Filesystem MCP 可能接触敏感文件 |
| 💸 **Context 消耗巨大** | 5 个 Server 58 个工具 = 55,000+ tokens |
| 😴 **被动架构** | 只能等待调用，不能主动编码工作流 |

### 3.5 MCP 的 Context 问题（关键数据）

```
5 个 MCP Server（58 个工具）= ~55,000 tokens（占 200K 模型的 27%）
3 个 Server（GitHub + Playwright + IDE）= 143K tokens（占 72%）
```

**解决方案**：Anthropic Tool Search 可减少 85% 的 MCP token 开销。

---

## 四、Plugins — Agent 的工具包

### 4.1 本质

```
Plugin = 封装好的功能扩展包 = Skills + MCP + Agents + Hooks + LSP 的打包单元
```

### 4.2 Claude Code Plugin 结构

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 元数据 + 配置
├── commands/                 # 斜杠命令
├── agents/                   # 子 Agent
├── skills/                   # Agent Skills
├── hooks/                    # 生命周期钩子
├── .mcp.json                # MCP Server 配置
└── .lsp.json                # LSP Server 配置
```

### 4.3 核心优势

| 优势 | 说明 |
|------|------|
| 📦 **打包分发** | npm for AI 配置，一键安装 |
| 🔄 **版本管理** | 支持语义化版本控制 |
| 🏪 **市场发现** | Marketplace 注册中心 |
| 👥 **团队共享** | 统一团队的 AI 工具链 |

### 4.4 核心局限

| 局限 | 说明 |
|------|------|
| 🔒 **平台锁定** | Copilot Plugin ≠ Claude Plugin ≠ Gemini Extension |
| 🧠 **Agent 理解弱** | 通常是输入-输出模式 |
| 🔀 **难组合** | 插件之间互相不知道存在 |

---

## 五、四者横向对比（含 Subagents）

### 5.1 八维雷达

| 维度 | Skills | MCP | Plugin | Subagent |
|------|--------|-----|--------|----------|
| 🧠 智能性提升 | ★★★★★ | ★★★ | ★★ | ★★★★ |
| 🤲 执行能力 | ☆ | ★★★★★ | ★★★ | ★★★★ |
| 🌐 通用性 | ★★★★★ | ★★★★★ | ★ | ★★★ |
| ⚙️ 部署难度 | ★（极低） | ★★★★（高） | ★（低） | ★★（中） |
| 🔧 扩展性 | ★★★★★ | ★★★★★ | ★★ | ★★★ |
| 💰 成本 | 极低（30-50 tok） | 极高（55K+ tok） | 中 | 中 |
| 📈 长期价值 | 极高 | 极高 | 中 | 高 |
| 🔄 上下文效率 | 极高（渐进式） | 极低（全量） | 中 | 高（隔离） |

### 5.2 Token 效率对比

| 扩展类型 | 基础开销 | 加载后开销 | 说明 |
|---------|---------|-----------|------|
| **Skill** | 30-50 tokens | <5K tokens | 渐进式加载 |
| **MCP Server** | 1-50K tokens | 相同 | 全量预加载* |
| **Plugin** | 各部分之和 | 变化 | 取决于内容 |
| **Hook** | 极小 | 极小 | Shell 执行 |
| **Command** | 极小 | 模板大小 | 用户调用 |

> *Anthropic Tool Search 可减少 85% 的 MCP 开销。

### 5.3 一句话总结

> **Skills 决定上限，MCP 决定行动力，Plugin 补齐生态缺口，Subagent 隔离复杂度。**

---

## 六、GitHub 仓库完整分类

> 详细版见 [GITHUB_ECOSYSTEM.md](./GITHUB_ECOSYSTEM.md)

### 6.1 MCP 仓库

| 仓库 | 类型 | Stars | 链接 |
|------|------|-------|------|
| **modelcontextprotocol/servers** | 官方 | 极高 | [GitHub](https://github.com/modelcontextprotocol/servers) |
| **modelcontextprotocol/spec** | 官方规范 | 极高 | [GitHub](https://github.com/modelcontextprotocol/spec) |
| **modelcontextprotocol/inspector** | 官方调试 | 高 | [GitHub](https://github.com/modelcontextprotocol/inspector) |
| **wong2/awesome-mcp-servers** | Awesome | 高 | [GitHub](https://github.com/wong2/awesome-mcp-servers) |
| **punkpeye/awesome-mcp-servers** | Awesome（1,000+） | 高 | [GitHub](https://github.com/punkpeye/awesome-mcp-servers) |
| **habitoai/awesome-mcp-servers** | Awesome | 中 | [GitHub](https://github.com/habitoai/awesome-mcp-servers) |
| **JustInCache/awesome-mcp-collection** | 精选 | 中 | [GitHub](https://github.com/JustInCache/awesome-mcp-collection) |
| **MaximPro/awesome-mcp-servers-meta** | Meta Index（7,260+） | 中 | [GitHub](https://github.com/MaximPro/awesome-mcp-servers-meta) |
| **WagnerAgent/awesome-mcp-servers-devops** | DevOps 专项 | 中 | [GitHub](https://github.com/WagnerAgent/awesome-mcp-servers-devops) |
| **collabnix/awesome-mcp-lists** | 容器化 | 中 | [GitHub](https://github.com/collabnix/awesome-mcp-lists) |
| **rdmgator12/awesome-healthcare-mcp-servers** | 医疗专项 | 低 | [GitHub](https://github.com/rdmgator12/awesome-healthcare-mcp-servers) |
| **punkpeye/awesome-mcp-clients** | 客户端 | - | [GitHub](https://github.com/punkpeye/awesome-mcp-clients) |
| **Infatoshi/x-mcp** | 独立 Server | 中 | [GitHub](https://github.com/Infatoshi/x-mcp) |
| **olgasafonova/miro-mcp-server** | 独立 Server（92 tools） | 中 | [GitHub](https://github.com/olgasafonova/miro-mcp-server) |
| **ricardodeazambuja/browser-mcp-server** | 独立 Server（63 tools） | 中 | [GitHub](https://github.com/ricardodeazambuja/browser-mcp-server) |
| **Dicklesworthstone/ultimate_mcp_server** | 全能 Server | 高 | [GitHub](https://github.com/dicklesworthstone/ultimate_mcp_server) |

### 6.2 Skills 仓库

| 仓库 | 类型 | Stars | Skills 数 | 链接 |
|------|------|-------|----------|------|
| **VoltAgent/awesome-agent-skills** | 通用 | ~9.1k | 1,424+ | [GitHub](https://github.com/VoltAgent/awesome-agent-skills) |
| **VoltAgent/awesome-openclaw-skills** | OpenClaw | ~49.9k | 5,400+ | [GitHub](https://github.com/VoltAgent/awesome-openclaw-skills) |
| **ComposioHQ/awesome-claude-skills** | Claude | 高 | 1,000+ | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills) |
| **alirezarezvani/claude-skills** | Claude 全平台 | ~13k | 232+ | [GitHub](https://github.com/alirezarezvani/claude-skills) |
| **Orchestra-Research/AI-Research-SKILLs** | AI 研究 | ~7.5k | - | [GitHub](https://github.com/Orchestra-Research/AI-Research-SKILLs) |
| **heilcheng/awesome-agent-skills** | 通用 | 中 | - | [GitHub](https://github.com/heilcheng/awesome-agent-skills) |
| **gmh5225/awesome-skills** | 通用 | 中 | - | [GitHub](https://github.com/gmh5225/awesome-skills) |
| **karanb192/awesome-claude-skills** | Claude | 中 | 50+ | [GitHub](https://github.com/karanb192/awesome-claude-skills) |
| **travisvn/awesome-claude-skills** | Claude | 中 | - | [GitHub](https://github.com/travisvn/awesome-claude-skills) |
| **itgoyo/awesome-agent-skills** | 通用 | 中 | - | [GitHub](https://github.com/itgoyo/awesome-agent-skills) |
| **sjkncs/awesome-openclaw-skills** | OpenClaw | 中 | 1,715+ | [GitHub](https://github.com/sjkncs/awesome-openclaw-skills) |
| **sundial-org/awesome-openclaw-skills** | OpenClaw | 中 | - | [GitHub](https://github.com/sundial-org/awesome-openclaw-skills) |
| **EthanYolo01/Awesome-OpenClaw** | OpenClaw 综合 | 中 | - | [GitHub](https://github.com/EthanYolo01/Awesome-OpenClaw) |
| **evgyur/awesome-openclaw** | OpenClaw 综合 | 中 | - | [GitHub](https://github.com/evgyur/awesome-openclaw) |
| **win4r/OpenClaw-Skill** | OpenClaw Skill | 311 | - | [GitHub](https://github.com/win4r/OpenClaw-Skill) |
| **scienceaix/agentskills** | 生态+学术 | 低 | - | [GitHub](https://github.com/scienceaix/agentskills) |
| **DiversioTeam/agent-skills-marketplace** | 市场 | - | - | [GitHub](https://github.com/DiversioTeam/agent-skills-marketplace) |

### 6.3 Plugin 仓库

| 仓库 | 类型 | 链接 |
|------|------|------|
| **github/awesome-copilot** | Copilot 官方 | [GitHub](https://github.com/github/awesome-copilot) |
| **github/copilot-plugins** | Copilot 注册表 | [GitHub](https://github.com/github/copilot-plugins) |
| **ComposioHQ/awesome-claude-plugins** | Claude 插件 | [GitHub](https://github.com/ComposioHQ/awesome-claude-plugins) |
| **rohitg00/awesome-claude-code-toolkit** | Claude 工具包（176+ plugins） | [GitHub](https://github.com/rohitg00/awesome-claude-code-toolkit) |
| **jeremylongshore/claude-code-plugins-plus-skills** | Claude 插件（432+） | [GitHub](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) |
| **quemsah/awesome-claude-plugins** | Claude Top 100 | [GitHub](https://github.com/quemsah/awesome-claude-plugins) |
| **EthanYolo01/Awesome-OpenClaw** | OpenClaw 综合 | [GitHub](https://github.com/EthanYolo01/Awesome-OpenClaw) |
| **henrikrexed/openclaw-observability-plugin** | OpenClaw 可观测性 | [GitHub](https://github.com/henrikrexed/openclaw-observability-plugin) |

### 6.4 Agent 框架

| 框架 | Stars | Skills | MCP | Plugin | Subagent | 链接 |
|------|-------|--------|-----|--------|----------|------|
| **Claude Code** | 极高 | ✅ | ✅ | ✅ | ✅ | [GitHub](https://github.com/anthropics) |
| **Codex CLI** | ~87.6k | ✅ | ❌ | ❌ | ✅ | [GitHub](https://github.com/openai/codex) |
| **Gemini CLI** | ~105k | ✅ | ✅ | ✅ Ext | ✅ | [GitHub](https://github.com/google-gemini/gemini-cli) |
| **OpenClaw** | ~49.9k | ✅ | ✅ | ✅ | ✅ | [GitHub](https://github.com/openclaw/openclaw) |
| **Cursor** | 极高 | ✅ Rules | ✅ | ❌ | ❌ | [GitHub](https://github.com/cursor) |
| **Cline** | 高 | ✅ | ✅ | ❌ | ❌ | [GitHub](https://github.com/cline/cline) |
| **OpenHands** | 高 | ✅ | ✅ | ❌ | ✅ | [GitHub](https://github.com/OpenHands/OpenHands) |
| **GitHub Copilot** | 极高 | ✅ | ✅ | ✅ | ✅ | [GitHub](https://github.com/github/copilot) |
| **OpenAI Agents SDK** | ~12k | ✅ | ❌ | ❌ | ✅ | [GitHub](https://github.com/openai/agents) |
| **Google ADK** | ~8k | ✅ | ❌ | ❌ | ✅ | [GitHub](https://github.com/google/generative-ai-python) |
| **AutoGen** | ~50k | ❌ | ❌ | ❌ | ✅ | [GitHub](https://github.com/microsoft/autogen) |

---

## 七、主流 Agent 框架内部架构对比

### 7.1 能力矩阵

| 能力 | Claude Code | Codex CLI | Gemini CLI | Copilot | Cursor | OpenClaw | OpenHands |
|------|------------|-----------|------------|---------|--------|----------|-----------|
| **Skills** | ✅ 双级别 | ✅ 单级别 | ✅ 单级别 | ✅+Instructions | ✅ Rules | ✅ 单级别 | ✅ 单级别 |
| **MCP** | ✅ stdio+HTTP | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Memory** | CLAUDE.md | AGENTS.md | GEMINI.md | copilot-instructions | .cursorrules | - | - |
| **Plugin** | ✅ | ❌ | Extensions | ✅ Marketplace | ❌ | ✅ | ❌ |
| **Subagent** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Hooks** | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Tool Search** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 7.2 演进趋势

```
2024: MCP 元年 → 所有工具都走 MCP → Context 爆炸
2025: Skills 崛起 → 渐进式披露解决 Context 问题 → Skills ≠ MCP 成为共识
2026: 三层融合 + Subagent 兴起 → CLI+Skills 替代 MCP(stdio) → MCP(HTTP) 留存企业
```

---

## 八、什么时候该用哪个

### 决策树

```
需要给 Agent 添加新能力
    │
    ├─ 是"怎么做"的问题？（流程/规范/最佳实践）
    │   └─ ✅ 写 Skill（SKILL.md）
    │
    ├─ 是"能不能做"的问题？（需要操作外部系统）
    │   ├─ 需要实时数据？→ ✅ 用 MCP Server
    │   └─ 只需要执行命令？→ ✅ 用 CLI + Skill 包装
    │
    ├─ 是"分发和打包"的问题？（需要团队共享）
    │   └─ ✅ 打包成 Plugin
    │
    ├─ 是"隔离执行"的问题？（任务需要独立 context）
    │   └─ ✅ 用 Subagent
    │
    └─ 是"生态缺口"的问题？（某个特定服务）
        ├─ 有现成 MCP Server？→ ✅ 安装 MCP
        ├─ 有现成 Plugin？→ ✅ 安装 Plugin
        └─ 都没有？→ ✅ 写 Skill + 包装 CLI
```

### 实际场景对照

| 场景 | 最佳选择 | 为什么 |
|------|---------|--------|
| 统一团队代码规范 | Skill | 只是流程指导 |
| Agent 操作 GitHub | MCP | 需要真正的 API 调用 |
| 团队共享 AI 工具链 | Plugin | 需要打包和分发 |
| 复杂多步部署 | Skill + MCP | Skill 编排 + MCP 执行 |
| 隔离代码搜索 | Subagent | 避免污染主 context |

---

## 九、最优组合

### 能力提升模型

```
仅模型                    ≈ 1x
模型 + Plugin             ≈ 2x
模型 + MCP                ≈ 5x
模型 + Skills             ≈ 8x
模型 + Skills + MCP + Memory ≈ 20x+
```

### 推荐架构

```
用户请求 → Planner Skill → Memory → RAG → MCP → Plugin → 结果验证
```

### 最小化配置（推荐起步）

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
```

```markdown
// .claude/CLAUDE.md
# Project: My App
- Use TypeScript strict mode
- Run `npm test` before committing
```

```markdown
// .claude/skills/deploy/SKILL.md
---
name: deploy
description: Deploy to production
---
1. Run full test suite
2. Build production bundle
3. Deploy to staging first
4. Run smoke tests
5. Promote to production
```

---

## 十、2026 年趋势

| 趋势 | 说明 |
|------|------|
| 🔥 OpenClaw Skills 爆发 | 49.9k stars，5,400+ Skills |
| 🔒 Skills 安全独立 | OWASP Agent Skills Top 10 |
| 🔄 CLI+Skills 替代 MCP(stdio) | Perplexity 公开弃用 MCP(stdio) |
| 🏢 MCP(HTTP) 留存企业 | 集中管理/OAuth/审计 |
| 📦 Skills 跨平台标准 | SKILL.md 被全平台采纳 |
| 👷 Subagent 普及 | Claude Code/Gemini/Codex 均支持 |
| 🏪 Plugin 市场成型 | Claude Code + Copilot Marketplace |

### 生态规模

| 指标 | 数量 |
|------|------|
| MCP Server 总数 | 14,000+ |
| OpenClaw Skills | 5,400+ |
| 通用 Agent Skills | 1,424+ |
| Claude Code Skills | 232+ |
| MCP SDK 月下载 | 9,700 万 |

---

## 参考资料

### 官方仓库
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — 官方 MCP Reference Servers
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — 1,424+ Agent Skills
- [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 5,400+ OpenClaw Skills
- [github/awesome-copilot](https://github.com/github/awesome-copilot) — Copilot 官方 Skills

### 深度文章
- [Skills vs MCP vs Plugins vs Subagents](https://awesomeskill.ai/blog/skills-vs-mcp-vs-plugins-vs-subagents)
- [Claude Code Skills vs MCP vs Plugins](https://www.morphllm.com/claude-code-skills-mcp-plugins)
- [Agent Skills, Plugins and Marketplace](https://chris-ayers.com/posts/agent-skills-plugins-marketplace)
- [Agent Skills Distribution Guide](https://gist.github.com/zoharbabin/cf5ab80b2b0af50e34328b5eb2bfdc93)

---

*最后更新：2026-07-07 | 数据来源：GitHub 全网检索，63+ 个仓库*
