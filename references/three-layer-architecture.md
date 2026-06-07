# 三层能力架构：Skills / MCP / Plugin

## 总览

Agent 领域的三层能力模型，每一层解决的问题完全不同：

```
用户请求
    ↓
┌─────────────────────────┐
│  Skills (大脑经验)       │ ← 告诉 Agent 怎么做
│  Prompt + Workflow      │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  RAG (长期记忆检索)      │ ← 历史经验
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  Planner Skill           │ ← 任务规划
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  MCP (手和脚)            │ ← 让 Agent 能做
│  Tool Execution         │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  Plugin (特殊工具)       │ ← 增加某个能力
│  Platform-specific      │
└────────┬────────────────┘
         ↓
    结果验证 & 输出
```

## 详细对比

### Skills — 大脑经验

**本质：** Prompt + Workflow + Best Practice + 经验

**运行方式：** Agent 加载 SKILL.md 后，按其中的指导进行推理和操作

**优点：**
- 提升推理质量：有 Skill 像高级工程师，没 Skill 像实习生
- 成本极低：只是 Prompt，不需要额外资源
- 易迁移：GPT/Claude/Gemini/GLM 全部可用

**缺点：**
- 不能执行：只会说"应该这样做"，不会"真的去做"
- 容易过时：K8s 2024 教程 2026 可能过期
- 容易 Prompt 污染：Skill 太多会冲突、覆盖、遗忘

**典型 Skill 结构：**
```yaml
---
name: devops-deploy
description: VPS 部署最佳实践
---

# DevOps 部署 Skill

## 触发条件
- 用户请求部署到 VPS
- 需要构建和发布

## 执行流程
1. 分析代码和依赖
2. 构建项目
3. 运行测试
4. 部署到目标
5. 验证服务
6. 回滚方案

## 注意事项
- 始终先备份
- 使用蓝绿部署
- 检查回滚脚本
```

### MCP — 手和脚

**本质：** 工具调用标准协议（Model Context Protocol）

**运行方式：** 独立进程，通过 JSON-RPC 与 Agent 通信

**优点：**
- 通用：一次开发，全 Agent 使用
- 工具丰富：GitHub/Docker/PostgreSQL/Browser/Slack
- 自主能力强：计划→执行→验证→修复 闭环

**缺点：**
- 需要部署：Node/Python/Docker 经常需要
- 权限管理复杂：Filesystem MCP 可能接触敏感文件
- 工具质量参差不齐

**MCP Server 结构：**
```json
{
  "name": "server-filesystem",
  "version": "1.0.0",
  "tools": [
    {
      "name": "read_file",
      "description": "Read a file from disk",
      "parameters": { "path": "string" }
    },
    {
      "name": "write_file",
      "description": "Write a file to disk",
      "parameters": { "path": "string", "content": "string" }
    }
  ]
}
```

### Plugin — 特殊工具

**本质：** 封装好的功能模块

**运行方式：** 安装后直接提供 API/CLI/GUI

**优点：**
- 开箱即用：安装即可
- 用户门槛低：适合普通人
- 某些场景体验很好：Jira/Notion/Slack 插件

**缺点：**
- 不通用：很多只能在某个平台
- Agent 理解较弱：通常输入→输出模式
- 难组合：插件之间互相不知道存在

## 组合效果

```
仅模型                      ≈  1x
模型 + Plugin               ≈  2x
模型 + MCP                  ≈  5x
模型 + Skills               ≈  8x
模型 + Skills + MCP + Memory ≈ 20x+
```

## 最优组合（2026 年标准）

```
LLM
  + Skills（知识+流程）
  + Memory（长期记忆）
  + MCP（工具执行）
  + Plugin（生态补充）
  + RAG（知识检索）
```

## 实际场景示例

**用户说："帮我分析 GitHub 项目并部署到 VPS"**

| 缺少什么 | 结果 |
|---------|------|
| 没有 Skills | Agent 知道要部署，但不知道最佳流程 |
| 没有 MCP | Agent 知道流程，但无法操作 GitHub |
| 没有 Plugin | Agent 能操作 GitHub，但无法调用特殊服务 |

## 与框架的关系

| 框架 | Skills | MCP | Plugin |
|------|--------|-----|--------|
| **Claude Code** | CLAUDE.md + Skills | ✅ 原生支持 | Subagents |
| **Hermes Agent** | SKILL.md | ✅ 原生支持 | plugins/ |
| **OpenClaw** | SKILL.md | ✅ 原生支持 | plugins/ |
| **Cursor** | Rules | ✅ 扩展 | Extensions |
| **OpenAI Codex** | AGENTS.md | ✅ 原生支持 | Tools |
| **Cline** | Rules | ✅ 扩展 | MCP Servers |
