# Skills 深度解析

## 什么是 Skills

**Skills** 不是代码，不是工具。它的本质是：

> **Prompt + Workflow + Best Practice + 经验**

一个 Skill 告诉 Agent：
- 遇到某种任务时，*应该按什么步骤做*
- *先做什么、再做什么*
- *有哪些坑要避开*
- *有哪些质量门禁要过*

---

## Skills 的格式

### SKILL.md 标准格式（2026 主流）

所有主流 Agent（Claude Code、Codex、Cursor、Gemini CLI）都遵守 [AGENTS.md](https://agents.md) 开放标准：

```yaml
---
name: devops-deploy
description: 标准 DevOps 部署流程：分析→构建→测试→部署→验证→回滚
trigger: 当用户提到部署、发布、上线(DEPLOY)
model: any
---

# DevOps Deploy Skill

## 流程
1. **代码分析** — 检查代码质量、依赖、安全漏洞
2. **构建** — 执行构建命令
3. **测试** — 运行单元测试 + 集成测试
4. **部署** — 按目标环境推送
5. **验证** — 健康检查 + smoke test
6. **回滚方案** — 准备回滚脚本

## 坑
- 部署前务必确认数据库迁移兼容性
- 生产环境禁止直接 merge 到 main
```

---

## Skills 的类型

### 按触发方式

| 类型 | 例子 | 说明 |
|------|------|------|
| **自动加载** | 代码审查 Skill | Agent 检测到 PR 时自动触发 |
| **用户手动** | `/review` 斜杠命令 | 用户主动调用 |
| **条件触发** | 某工具返回特定值时 | Agent 内部决策触发 |

### 按领域

| 领域 | 典型 Skills |
|------|-----------|
| **DevOps** | 部署流程、CI/CD、回滚、监控 |
| **网络** | VPN 配置、防火墙规则、DNS 管理 |
| **代码开发** | TDD、代码审查、重构、架构设计 |
| **数据科学** | ETL 流程、模型训练、数据清洗 |
| **安全** | 漏洞扫描、权限审计、密钥管理 |

---

## Skills 生态盘点（2026）

### 官方 Skills 仓库

| 来源 | 仓库 | 说明 |
|------|------|------|
| **Anthropic** | [anthropic/claude-code-skills](https://github.com/anthropics/claude-code/tree/main/skills) | 17 个官方 Skills |
| **VoltAgent** | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 社区最大，1000+ Skills |
| **Addy Osmani** | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 23 个生产级 Skills |
| **Skillmatic AI** | [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) | 索引型仓库 |

### 大厂官方 Skills

| 公司 | Skills | 用途 |
|------|--------|------|
| **Stripe** | 支付集成、Webhook、退款 | 金融 |
| **Vercel** | React 最佳实践、Web 设计规范 | 前端 |
| **Cloudflare** | Worker、DNS、CDN | 网络 |
| **Sentry** | 错误监控、性能追踪 | 可观测 |
| **Trail of Bits** | 安全审计 | 安全 |
| **Hugging Face** | 模型训练、数据集处理 | ML |
| **NVIDIA** | Megatron、TensorRT、CUDA | GPU 计算 |
| **Google/Gemini** | 官方 Gemini Skills | 通用 |

---

## Skills 的优点

| 优点 | 说明 |
|------|------|
| **🔺 提升推理质量** | 同一模型：有 Skill = 高级工程师 / 没 Skill = 实习生 |
| **💰 成本极低** | 几乎不消耗资源 — 只是 Prompt |
| **🔄 易迁移** | 一套 Skills 可以在 GPT / Claude / Gemini 之间复用 |
| **📦 轻量** | 纯文本文件，无需部署 |
| **🧩 可组合** | 多个 Skill 叠加效果 > 单一 Skill |

---

## Skills 的缺点

| 缺点 | 说明 |
|------|------|
| **❌ 不能执行** | 只告诉 Agent "应该怎么做"，不会真的去做 |
| **⏰ 容易过时** | 2024 的 K8s 教程在 2026 可能已过期 |
| **🧠 Prompt 污染** | Skill 太多会导致冲突、覆盖、遗忘 |
| **📏 质量参差** | 社区 Skills 质量不一，需要筛选 |

---

## Skills vs 传统 Prompt Engineering

| 维度 | 传统 Prompt | Skills |
|------|------------|--------|
| 结构 | 一次性对话 | 模块化、可组合 |
| 复用 | 每次重写 | 一键加载 |
| 编排 | 手动 | 自动条件触发 |
| 生态 | 孤立 | 社区共享 |
| 版本 | 无 | SKILL.md 可版本管理 |
