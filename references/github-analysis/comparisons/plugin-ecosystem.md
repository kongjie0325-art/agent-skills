# Plugin 生态 — Claude/Codex/IDE 插件

## 目录
- [一、Claude Code Plugin 市场](#一claude-code-plugin-市场)
- [二、OpenAI Codex Plugin](#二openai-codex-plugin)
- [三、IDE 扩展生态](#三ide-扩展生态)
- [四、Plugin 对比总表](#四plugin-对比总表)

---

## 一、Claude Code Plugin 市场

### 市场概况
- **发布**: 2026-01-30
- **入口**: `/plugin marketplace` 命令
- **数量**: 数十个官方 + 社区 Plugin

### 热门 Plugins

| Plugin | 说明 | 包含内容 |
|--------|------|----------|
| Superpowers | 完整 multi-agent 开发 | Skills + Sub-agents + Hooks |
| Firecrawl | 网页抓取 | MCP + Skill |
| Code Review | 代码审查 | Skill + Agent |
| Security Scan | 安全扫描 | Skill + Hook |
| Deploy | 部署流水线 | Skill + MCP |

### Plugin 生命周期
```
/plugin marketplace add <source>   # 添加市场源
/plugin list                        # 浏览可用 Plugins
/plugin install <name>              # 安装
/plugin uninstall <name>            # 卸载
/plugin update <name>               # 更新
```

---

## 二、OpenAI Codex Plugin

### 概况
- **发布**: 2025-06
- **入口**: UI 左上角 Plugins 按钮
- **创建门槛**: 较高（需要技术知识）

### 与 Claude Code 的区别

| 维度 | Claude Code | OpenAI Codex |
|------|-------------|--------------|
| **发现** | 命令行 + Marketplace | UI 浏览 |
| **安装** | 命令 | UI 点击 |
| **创建** | plugin.json | 无标准格式 |
| **分享** | Git/GitHub | GitHub |
| **技术门槛** | 中 | 高 |

### Codex 官方 Plugin 列表
- Google Drive（文件引用）
- Gmail（邮件扫描）
- Calendar（日程管理）
- Slack（消息）
- Figma（设计）
- 还有更多...

---

## 三、IDE 扩展生态

### VS Code 扩展

| 扩展 | Stars | 说明 |
|------|-------|------|
| Cline | 58.6K | AI 编码 Agent |
| Roo Code | 22.5K | AI 编码 Agent |
| GitHub Copilot | - | 代码补全 + Chat |
| Continue | 25K+ | 开源 AI 编码 |
| Codeium | - | 免费 AI 补全 |

### JetBrains 插件

| 插件 | 说明 |
|------|------|
| Claude Code | Anthropic 官方 |
| GitHub Copilot | GitHub 官方 |
| Codeium | 免费替代 |
| Cursor | AI-first IDE |

### 各 IDE 的"插件"机制对比

| IDE | 扩展机制 | MCP 支持 | Skills 支持 |
|-----|----------|----------|------------|
| VS Code | Extensions API | ✅ 扩展内置 | ✅ 通过扩展 |
| Cursor | .cursorrules + Extensions | ✅ 原生 | ✅ .cursorrules |
| Cline | .cline/skills/ + MCP | ✅ | ✅ SKILL.md |
| Roo Code | .roo/ + Extensions | 部分 | 部分 |
| JetBrains | Plugin SDK | 部分 | 部分 |

---

## 四、Plugin 对比总表

| 维度 | Claude Code Plugin | Codex Plugin | VS Code 扩展 | JetBrains Plugin |
|------|-------------------|-------------|-------------|-----------------|
| **打包格式** | plugin.json | 无标准 | extension package | JAR/XML |
| **包含内容** | Skills+Agents+Hooks+MCP | Skills+MCP | 任意代码 | 任意代码 |
| **安装方式** | 命令 | UI | Marketplace | Marketplace |
| **运行时** | Claude Code 内 | Codex 内 | VS Code 内 | JetBrains 内 |
| **Agent 集成** | 深度 | 深度 | 中 | 中 |
| **跨 IDE** | ❌ | ❌ | ❌ | ❌ |

---

**下一节 →** [../frameworks/claude-code.md](../frameworks/claude-code.md) — Claude Code 完整架构
