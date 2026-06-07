# Cline 完整架构分析

## 目录
- [一、架构总览](#一架构总览)
- [二、Skills 系统](#二skills-系统)
- [三、MCP 系统](#三mcp-系统)
- [四、Rules 系统](#四rules-系统)
- [五、自动模式](#五自动模式)

---

## 一、架构总览

```
┌──────────────────────────────────────────┐
│              Cline (VS Code 扩展)          │
│                                          │
│  [Chat/Plan Mode] → [Tool Execution]     │
│        ↕                  ↕               │
│    Skills(.cline/skills/)  MCP Servers    │
│        ↕                  ↕               │
│    .cursorRules        外部工具            │
│                                          │
│  安全: VS Code 沙箱 + 权限确认            │
└──────────────────────────────────────────┘
```

**Cline 特色**: 开源 VS Code 扩展，58.6K stars，最强 MCP 支持之一。

---

## 二、Skills 系统

### 位置
- `.cline/skills/` 目录
- SKILL.md 格式（与 Claude Code 兼容）

### 热门 Skills
| Skill | 安装量 | 说明 |
|-------|--------|------|
| code-reviewer | 447 | 代码审查 |
| git-commit-writer | 170 | Git 提交信息 |
| env-doctor | 86 | 环境诊断 |

### 触发方式
- 自动触发（基于 description）
- 手动触发（`/skill-name`）

---

## 三、MCP 系统

### 支持程度
- ✅ 原生 MCP 集成
- ✅ stdio + Streamable HTTP
- ✅ 自动发现
- ✅ 工具栏 UI 集成

### MCP 配置
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

---

## 四、Rules 系统

### .cursorrules / .cline/rules
- 项目级编码规范
- 每次会话自动加载
- 类似 Claude Code 的 CLAUDE.md

### 示例
```markdown
# .cursorrules

## 编码规范
- 使用 TypeScript strict mode
- 所有函数必须有返回类型
- 使用函数式编程风格
- 不用 any 类型
```

---

## 五、自动模式

### Auto-approve
- Cline 的标志性功能
- 可以在无需确认的情况下执行：
  - 文件读写
  - 终端命令
  - 浏览器操作

### 安全机制
- VS Code 沙箱隔离
- 敏感操作仍需确认
- 可扩展的权限系统

---

**下一节 →** [../frameworks/roo-code.md](../frameworks/roo-code.md) — Roo Code 完整架构
