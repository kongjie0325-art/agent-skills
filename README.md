# 🧠 Agent Skills Hub

> **"Skills = 大脑经验"** — 精选 AI Agent 技能库，让 Agent 知道怎么做。

## 📖 什么是 Skills？

Skills 本质是 **Prompt + Workflow + Best Practice + 经验**。

它们告诉 Agent 面对特定任务时的最佳流程、注意事项和操作步骤。不需要运行任何服务，只需要 Agent 加载对应的 SKILL.md。

**类比：** 同一个模型，有 Skill 像高级工程师，没 Skill 像实习生。

## 🏗️ 项目结构

```
agent-skills/
├── README.md              # 本文件
├── deploy.sh              # 一键部署脚本
├── skills/                # 精选 Skills 目录
│   ├── devops/            # 运维 & 部署
│   ├── github/            # GitHub 自动化
│   ├── software-dev/      # 软件开发
│   ├── research/          # 学术研究
│   ├── creative/          # 创意设计
│   ├── productivity/      # 生产力工具
│   ├── media/             # 媒体处理
│   └── mcp-guide/         # MCP 使用指南
└── references/            # 参考资料
    ├── three-layer-architecture.md
    └── skills-vs-mcp-vs-plugin.md
```

## 🚀 快速部署

### 方式一：一键脚本（推荐）

```bash
git clone https://github.com/kongjie0325-art/agent-skills.git
cd agent-skills
bash deploy.sh
```

### 方式二：手动安装

```bash
# 克隆到任意位置
git clone https://github.com/kongjie0325-art/agent-skills.git
cd agent-skills

# 复制 Skills 到 Hermes Agent skills 目录
cp -r skills/* ~/.hermes/skills/

# 或软链接（方便更新）
ln -s $(pwd)/skills/devops ~/.hermes/skills/devops
ln -s $(pwd)/skills/github ~/.hermes/skills/github
# ... 按需链接
```

## 📦 Skills 清单

### 🏭 DevOps & 部署
| Skill | 说明 |
|-------|------|
| `devops/kanban-orchestrator` | 看板编排：任务分解 + 反诱惑规则 |
| `devops/kanban-worker` | 看板工作器：Pitfalls + 边界案例 |
| `devops/webhook-subscriptions` | Webhook 订阅：事件驱动 Agent 运行 |

### 🐙 GitHub 自动化
| Skill | 说明 |
|-------|------|
| `github/github-auth` | GitHub 认证：Token、SSH、gh CLI |
| `github/github-pr-workflow` | PR 生命周期：分支→提交→CI→合并 |
| `github/github-code-review` | 代码审查：Diff + 内联评论 |
| `github/github-issues` | Issue 管理：创建/分类/分配 |
| `github/github-repo-management` | 仓库管理：克隆/创建/Fork/发布 |

### 💻 软件开发
| Skill | 说明 |
|-------|------|
| `software-dev/systematic-debugging` | 4阶段根因调试 |
| `software-dev/test-driven-development` | TDD：RED-GREEN-REFACTOR |
| `software-dev/python-debugpy` | Python 调试：pdb + debugpy |
| `software-dev/node-inspect-debugger` | Node.js 调试：Chrome DevTools |
| `software-dev/subagent-driven-development` | 子代理驱动开发：2阶段审查 |
| `software-dev/requesting-code-review` | 预提交审查：安全扫描+质量门 |
| `software-dev/writing-plans` | 实施计划编写 |
| `software-dev/plan` | 计划模式 |
| `software-dev/spike` | 快速验证实验 |

### 🔬 学术研究
| Skill | 说明 |
|-------|------|
| `research/arxiv` | arXiv 论文搜索 |
| `research/blogwatcher` | 博客/RSS 监控 |
| `research/llm-wiki` | Karpathy LLM Wiki 知识库 |
| `research/polymarket` | Polymarket 市场查询 |
| `research/research-paper-writing` | ML 论文写作（NeurIPS/ICML/ICLR） |

### 🎨 创意设计
| Skill | 说明 |
|-------|------|
| `creative/architecture-diagram` | 云/架构 SVG 图 |
| `creative/ascii-art` | ASCII 艺术 |
| `creative/baoyu-comic` | 知识漫画（教育/传记/教程） |
| `creative/baoyu-infographic` | 信息图（21布局×21风格） |
| `creative/claude-design` | 一次性 HTML 设计稿 |
| `creative/excalidraw` | 手绘风 Excalidraw 图 |
| `creative/humanizer` | 文本人性化 |
| `creative/manim-video` | 3Blue1Brown 数学动画 |
| `creative/p5js` | p5.js 创意编程 |
| `creative/pixel-art` | 像素画 |

### 📋 生产力
| Skill | 说明 |
|-------|------|
| `productivity/airtable` | Airtable REST API |
| `productivity/google-workspace` | Google Workspace（Gmail/Calendar/Drive）|
| `productivity/linear` | Linear 项目管理 |
| `productivity/notion` | Notion API |
| `productivity/obsidian` | Obsidian 笔记 |
| `productivity/powerpoint` | PPT 创建/编辑 |
| `productivity/nano-pdf` | PDF 编辑 |
| `productivity/ocr-and-documents` | OCR 文档提取 |
| `productivity/maps` | 地图/POI/路线 |

### 🎬 媒体
| Skill | 说明 |
|-------|------|
| `media/youtube-content` | YouTube 转录→摘要 |
| `media/spotify` | Spotify 播放管理 |
| `media/gif-search` | GIF 搜索/下载 |
| `media/songsee` | 音频频谱分析 |
| `media/heartmula` | Suno 类歌曲生成 |

## 📊 Skills 对比 MCP vs Plugin

| 维度 | Skills | MCP | Plugin |
|------|--------|-----|--------|
| 本质 | 知识+流程模板 | 工具调用标准 | 功能扩展 |
| 作用 | 告诉怎么做 | 让能做 | 增加能力 |
| 智能性提升 | ★★★★★ | ★★★ | ★★ |
| 执行能力 | ☆ | ★★★★★ | ★★★ |
| 通用性 | ★★★★★ | ★★★★★ | ★ |
| 部署难度 | 极低 | 中 | 低 |
| 成本 | 极低 | 中 | 中 |

## 🔗 相关项目

- **[agent-mcp](https://github.com/kongjie0325-art/agent-mcp)** — MCP Server 精选 + 部署
- **[agent-plugins](https://github.com/kongjie0325-art/agent-plugins)** — Plugin 精选 + 部署

## 📄 License

MIT
