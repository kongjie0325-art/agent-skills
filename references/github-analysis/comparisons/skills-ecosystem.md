# Skills 生态 — SKILL.md 标准、安装方式、热门 Skills

## 目录
- [一、SKILL.md 标准](#一skillmd-标准)
- [二、安装方式对比](#二安装方式对比)
- [三、热门 Skills 分类](#三热门-skills-分类)
- [四、Skills 编写最佳实践](#四skills-编写最佳实践)

---

## 一、SKILL.md 标准

### 标准演进
```
2025-10  Anthropic 发布 Agent Skills（API + Claude Code）
2025-10  SKILL.md 格式发布
2025-11  Claude Code 支持自定义 Skills
2026-01  Plugin 打包标准发布
2026-03  OpenAI Codex 支持 SKILL.md
2026-04  Cursor/Gemini/Copilot 全面采纳
```

### 当前标准状态
- **维护方**: Anthropic → Linux Foundation AAIF（可能迁移）
- **格式**: YAML frontmatter + Markdown body
- **兼容性**: Claude Code / Codex / Cursor / Gemini CLI / GitHub Copilot
- **最小实现**: 一个 `SKILL.md` 文件

---

## 二、安装方式对比

| 工具 | 个人安装 | 项目安装 | 市场安装 | CLI 安装 |
|------|----------|----------|----------|----------|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` | `/plugin marketplace` | `npx skills add` |
| **Codex** | `~/.codex/skills/` | `.codex/skills/` | UI 浏览 | `$skill-installer` |
| **Cursor** | `~/.cursor/skills/` | `.cursor/skills/` | 无 | 手动 |
| **Cline** | - | `.cline/skills/` | 无 | 手动 |
| **Roo Code** | - | `.roo/` | 无 | 手动 |
| **Gemini CLI** | `~/.gemini/skills/` | `.gemini/skills/` | 无 | `gemini skills add` |

---

## 三、热门 Skills 分类

### 📋 表格格式（Telegram 兼容）

**编码规范类**
| Skill | Stars | 安装量 | 说明 |
|-------|-------|--------|------|
| Superpowers | 40.9K | 3.1K forks | 完整 multi-agent 开发工作流 |
| Karpathy's Guidelines | 144K | - | 4 条 LLM 编码原则 |
| Code Review Checklist | - | 447 | 代码审查检查表 |
| TDD | - | - | 测试驱动开发 |

**设计类**
| Skill | Stars | 安装量 | 说明 |
|-------|-------|--------|------|
| Frontend Design | - | 277K+ | 前端设计规范（Anthropic 官方）|
| Vercel Web Design | - | - | 100+ 规则审计 |
| Vercel React | - | - | React 最佳实践 |

**DevOps 类**
| Skill | Stars | 安装量 | 说明 |
|-------|-------|--------|------|
| Deploy Checklist | - | - | 部署检查清单 |
| Git Commit Writer | - | 170 | Git 提交信息编写 |
| Env Doctor | - | 86 | 环境诊断 |

**文档类**
| Skill | Stars | 安装量 | 说明 |
|-------|-------|--------|------|
| PDF Processing | - | - | PDF 处理（Anthropic 官方）|
| PPTX Creation | - | - | PPT 制作（Anthropic 官方）|
| DOCX Processing | - | - | Word 文档（Anthropic 官方）|

**上下文工程类**
| Skill | Stars | 安装量 | 说明 |
|-------|-------|--------|------|
| Agent Skills for Context Engineering | 16.1K | 1.3K forks | 基础+架构+操作 完整 Skills |
| Skill Creator | - | - | 创建新 Skill 的 Skill |

---

## 四、Skills 编写最佳实践

### 1. Description 是触发器的关键
```yaml
# ❌ 太模糊
description: 帮助处理文档

# ✅ 精确
description: 当用户提到 PDF、表单、文档提取、合并文件时使用。适用于 PDF 处理场景。
```

### 2. 脚本执行优于生成代码
```yaml
# ✅ 推荐：包含脚本，直接运行
---
name: validate-config
---
使用 scripts/validate.py 验证配置文件：
\```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate.py config.yaml
\```
```

### 3. 控制 Skill 体积
- SKILL.md 正文 < 5K tokens
- 大文档拆分为 REFERENCE.md 等按需加载
- 脚本代码不进上下文

### 4. 使用 paths 限制自动加载
```yaml
---
name: frontend-review
paths: "src/components/**/*.tsx"
---
```

### 5. 安全敏感的 Skill 禁用自动触发
```yaml
---
name: deploy
disable-model-invocation: true
---
```

---

**下一节 →** [../comparisons/mcp-ecosystem.md](../comparisons/mcp-ecosystem.md) — MCP 生态
