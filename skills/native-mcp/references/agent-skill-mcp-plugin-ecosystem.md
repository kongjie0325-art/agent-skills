# Agent Skills / MCP / Plugin 生态全景

> 2026-07-07 研究整理，基于 GitHub 43 个仓库的系统性检索
> 2026-07-07 补充用户框架（三层能力模型）和最优配置

## 核心定位速查

| 能力 | 本质 | 解决的问题 | 类比 | 格式 |
|------|------|-----------|------|------|
| **Skills** | 知识+流程模板+最佳实践 | 告诉 Agent 怎么做 | 大脑经验 | SKILL.md |
| **MCP** | 工具调用标准协议 | 让 Agent 能做 | 手和脚 | JSON-RPC 2.0 |
| **Plugin** | 封装好的功能扩展包 | 增加某个能力 | 特殊工具/工具包 | plugin.json |
| **Subagent** | 独立的专用 Agent 实例 | 隔离特定任务 | 专业工人 | .agent.md |

**一句话：Skills 决定上限，MCP 决定行动力，Plugin 决定功能补充，Subagent 隔离复杂度。**

## 用户框架：三层能力模型（2026 标准参考）

用户（kongjie0325-art）对三层模型有深入理解，视其为 2026 年标准架构参考。核心观点：

### 定位区别（无 X vs 有 X 的对比）

- **没有 Skills**：Agent 知道要部署，但不知道最佳流程
- **没有 MCP**：Agent 知道流程，但无法操作 GitHub
- **没有 Plugin**：Agent 能操作 GitHub，但无法调用某个特殊服务

### Skills 深度分析

**本质**：Prompt + Workflow + Best Practice + 经验

**优点**：
1. 提升推理质量（有 Skill = 高级工程师，没 Skill = 实习生）
2. 成本低（几乎不用资源，只是 Prompt）
3. 易迁移（GPT/Claude/Gemini/GLM 全部可用）

**缺点**：
1. 不能执行（只会说"应该这样做"，不会"真的去做"）
2. 容易过时（K8s 2024 教程到 2026 可能过期）
3. 容易 Prompt 污染（Skill 太多导致冲突/覆盖/遗忘）

### MCP 深度分析

**本质**：工具调用标准协议，解决"怎么执行"

**优点**：
1. 通用（一次开发，全 Agent 使用）
2. 工具丰富（GitHub/Docker/PostgreSQL/Redis/Browser/Slack）
3. Agent 自主能力强（计划→执行→验证→修复→闭环）

**缺点**：
1. 需要部署（Node/Python/Docker 经常需要）
2. 权限管理复杂（Filesystem MCP 可能接触敏感文件）
3. 工具质量参差不齐

### Plugin 深度分析

**本质**：封装好的功能扩展（天气/地图/翻译等）

**优点**：
1. 开箱即用
2. 用户门槛低
3. 某些场景体验很好（Jira/Notion/Slack 插件）

**缺点**：
1. 不通用（很多只能在某个平台）
2. Agent 理解较弱（通常只是输入/输出模式）
3. 难组合（插件之间互相不知道存在）

### 横向比较

| 指标 | Skills | MCP | Plugin |
|------|--------|-----|--------|
| 智能性提升 | ★★★★★ | ★★★ | ★★ |
| 执行能力 | ☆ | ★★★★★ | ★★★ |
| 通用性 | ★★★★★ | ★★★★★ | ★ |
| 部署难度 | ★ | ★★★★ | ★ |
| 扩展性 | ★★★★★ | ★★★★★ | ★★ |
| 成本 | 极低 | 中 | 中 |
| 长期价值 | 极高 | 极高 | 中 |

### 能力倍增效应（经验值）

| 配置 | 相对能力 |
|------|---------|
| 仅模型 | ≈ 1x |
| 模型 + Plugin | ≈ 2x |
| 模型 + MCP | ≈ 5x |
| 模型 + Skills | ≈ 8x |
| 模型 + Skills + MCP + Memory | ≈ 20x+ |

### 最优架构组合

```
用户 → Planner Skill → Memory → RAG → MCP → Plugin → 结果验证
```

完整栈：LLM + Skills + Memory + MCP + Plugin + RAG

### 用户的最优配置（开发/VPS/自动化场景）

基于用户长期经验（VPS 运维、GitHub 自动化、Shadowrocket 规则、AI 工作流、Codex、Claude Code）：

**不是堆插件，而是**：
- GPT-5 / Claude
- 长期记忆 (Memory)
- DevOps Skills
- Network Skills
- GitHub MCP
- Filesystem MCP
- Browser MCP
- Docker MCP
- Search 插件

**关键洞察**：很多人以为 MCP > Skills，实际上不一定。GPT 无工具有优秀 Skills → 90 分方案；Agent 有 20 个 MCP 无 Skills → 40 分方案然后疯狂执行。

## GitHub 仓库完整分类

### Skills 仓库（15 个）

**通用 Agent Skills（跨平台）：**
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — ~9.1k stars, 1,424+ Skills，含 Anthropic/Google/Stripe/Cloudflare 等官方 Skills
- [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — ~49.9k stars, 5,400+ OpenClaw Skills
- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) — 社区策展，配合 agent-skill.co
- [scienceaix/agentskills](https://github.com/scienceaix/agentskills) — Skills 生态+MCP+学术研究+Agent 框架

**Claude 专属：**
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — ~13k stars, 232+ Skills
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) — ~7.5k stars, AI 研究 Skills

**Skills 市场：**
- [DiversioTeam/agent-skills-marketplace](https://github.com/DiversioTeam/agent-skills-marketplace) — 开放标准市场
- [awesomeskill.ai](https://awesomeskill.ai) — Agent Skills 市场，支持 Claude/Codex/ChatGPT
- [skills.sh](https://github.com/anthropics/skills) — Open Agent Skills 目录

### MCP 仓库（10 个）

**官方：**
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — 官方 Reference Servers
- [modelcontextprotocol/spec](https://github.com/modelcontextprotocol/spec) — 协议规范

**Awesome 列表：**
- [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) — 精选 MCP Server
- [patriksimek/awesome-mcp-servers-2](https://github.com/patriksimek/awesome-mcp-servers-2) — 21 个分类
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — 1,000+ 精选 Server

**市场：**
- [glama.ai](https://glama.ai) — MCP Server 目录（1000+ 评分）
- [mcp.so](https://mcp.so) — MCP Server 搜索

### Plugin 仓库（7 个）

- [github/awesome-copilot](https://github.com/github/awesome-copilot) — Copilot 官方 Skills/Plugins
- [github/copilot-plugins](https://github.com/github/copilot-plugins) — Copilot 官方插件注册
- [ComposioHQ/awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins) — Claude Code 插件
- [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) — 135 agents + 35 skills + 176+ plugins

### Agent 框架（8 个）

| 框架 | Skills | MCP | Plugin | Subagent |
|------|--------|-----|--------|----------|
| Claude Code | yes | yes | yes | yes |
| Codex CLI | yes | no | no | yes |
| Gemini CLI | yes | yes | yes Extensions | yes |
| OpenClaw | yes | yes | yes | yes |
| GitHub Copilot | yes | yes | yes | yes |
| Cursor | yes Rules | yes | no | no |
| Cline | yes | yes | no | no |
| OpenHands | yes | yes | no | yes |

## Token 效率关键数据

| 扩展类型 | 基础开销 | 加载后开销 |
|---------|---------|-----------|
| Skill | 30-50 tokens | <5K tokens（渐进式） |
| MCP Server | 1-50K tokens | 相同（全量预加载） |
| Plugin | 各部分之和 | 变化 |
| Subagent | 中 | 高（完全隔离） |

**关键发现：** 5 个 MCP Server（58 个工具）= 55,000+ tokens（27% of 200K context）。Anthropic Tool Search 可减少 85% 开销。

## Skills 标准发现路径

| 工具 | 仓库级 | 用户级 | 全局 |
|------|--------|--------|------|
| Claude Code | `.github/skills/` | `.claude/skills/` | `~/.claude/skills/` |
| Codex CLI | `.agents/skills/` | - | `~/.agents/skills/` |
| Gemini CLI | `.gemini/skills/` | - | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | - | `~/.copilot/skills/` |
| Cursor | `.cursor/rules/` | - | `~/.cursor/rules/` |
| OpenClaw | `skills/` | - | `~/.openclaw/skills/` |

## 2026 年趋势

1. CLI + Skills 模式正在替代 MCP over stdio（Perplexity 已公开弃用 MCP stdio）
2. MCP over HTTP 仍是企业首选（集中管理、OAuth、审计日志）
3. Agent Skills 安全成为独立领域（OWASP AST10）
4. Skills + MCP + Plugin 三层融合成为标准架构
5. 生态规模：14,000+ MCP Server，5,400+ OpenClaw Skills，1,424+ 通用 Skills

## 参考资料

- [Skills vs MCP vs Plugins vs Subagents](https://awesomeskill.ai/blog/skills-vs-mcp-vs-plugins-vs-subagents) — Awesome Skills 团队
- [Claude Code Skills vs MCP vs Plugins](https://www.morphllm.com/claude-code-skills-mcp-plugins) — Morph
- [Agent Skills Distribution Guide](https://gist.github.com/zoharbabin/cf5ab80b2b0af50e34328b5eb2bfdc93) — Zohar Babin
- [Is MCP Dead? CLI and Skills for AI Agents](https://milvus.io/blog/is-mcp-dead-cli-and-skills-for-ai-agents.md) — Zilliz
