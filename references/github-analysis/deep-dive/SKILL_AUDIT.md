# 91 个 Hermes Skills 完整分类审计

> 逐个检查每个 Skill 的 SKILL.md 内容，精确分类

## 分类标准

| 类型 | 定义 | 判断依据 |
|------|------|---------|
| **🧠 Knowledge Skill** | 纯知识/流程/最佳实践 | 输出是"指导"，不绑定特定 CLI |
| **🔧 CLI Skill** | 对 CLI 工具的 Skill 化包装 | 核心功能依赖特定 CLI 命令 |
| **🎨 Creative Skill** | 生成物输出 | 输出是图片/HTML/文本艺术品 |
| **🤖 Delegate Skill** | 委派给子 Agent | 核心是 spawn 独立 Agent |
| **🍎 Platform Skill** | 平台独占 | 绑定 Apple/macOS 等特定平台 |
| **🔗 MCP Skill** | MCP 协议使用 | 唯一一个是 native-mcp |

## 完整清单

### 🧠 Knowledge Skills（38 个）

| # | Skill | 文件数 | 分类理由 |
|---|-------|-------|---------|
| 1 | github-auth | 10 | 认证流程指南，包含 token scope 检测、HTTPS/SSH 选择 |
| 2 | github-repo-management | 2 | 仓库创建/Fork/Release 操作流程 |
| 3 | github-pr-workflow | 5 | PR 分支→提交→CI→合并全流程 |
| 4 | github-code-review | 2 | PR 审查标准和行内评论流程 |
| 5 | github-issues | 3 | Issue 创建/分类/标签/分配流程 |
| 6 | systematic-debugging | 1 | 4 阶段根因调试方法论 |
| 7 | test-driven-development | 1 | TDD RED-GREEN-REFACTOR 方法论 |
| 8 | requesting-code-review | 1 | 提交前审查+安全扫描流程 |
| 9 | spike | 1 | 快速实验验证方法论 |
| 10 | plan | 1 | 计划模式（只写不执行） |
| 11 | writing-plans | 1 | 实现计划编写指南 |
| 12 | subagent-driven-development | 3 | 子 Agent 编排+2 阶段审查流程 |
| 13 | hermes-agent-skill-authoring | 1 | SKILL.md 编写规范 |
| 14 | kanban-orchestrator | 1 | 任务编排分解流程 |
| 15 | kanban-worker | 1 | Worker 避坑指南 |
| 16 | dogfood | 1 | 探索性 QA 方法论 |
| 17 | research-paper-writing | 55 | 论文写作全流程（设计→实验→提交） |
| 18 | arxiv | 2 | 论文搜索流程 |
| 19 | polymarket | 3 | 市场数据查询流程 |
| 20 | blogwatcher | 1 | RSS 监控流程 |
| 21 | llm-wiki | 1 | 知识库构建流程 |
| 22 | obsidian | 1 | 笔记管理流程 |
| 23 | himalaya | 3 | 邮件操作流程 |
| 24 | airtable | 1 | 数据库 CRUD 流程 |
| 25 | linear | 2 | 项目管理流程 |
| 26 | notion | 2 | 笔记数据库流程 |
| 27 | ocr-and-documents | 4 | OCR 提取流程 |
| 28 | nano-pdf | 1 | PDF 编辑流程 |
| 29 | powerpoint | 50 | PPT 制作流程 |
| 30 | google-workspace | 6 | Google Workspace 全流程 |
| 31 | maps | 2 | 地理编码/POI/路线查询流程 |
| 32 | teams-meeting-pipeline | 1 | 会议摘要流程 |
| 33 | webhook-subscriptions | 1 | Webhook 事件驱动流程 |
| 34 | codebase-inspection | 1 | 代码分析流程 |
| 35 | debugging-hermes-tui-commands | 1 | TUI 命令调试流程 |
| 36 | hermes-s6-container-supervision | 1 | 容器服务管理流程 |
| 37 | hermes-agent | 2 | Hermes 配置/扩展指南 |
| 38 | native-mcp | 1 | MCP 客户端使用指南 |

### 🔧 CLI Skills（28 个）

| # | Skill | 底层工具 | 分类理由 |
|---|-------|---------|---------|
| 1 | spotify | spotify-cli | 媒体播放 |
| 2 | xurl | xurl CLI | Twitter/X API |
| 3 | openhue | openhue CLI | Philips Hue 灯控 |
| 4 | minecraft-modpack-server | java + curseforge API | 游戏服务器 |
| 5 | pokemon-player | pyboy | GameBoy 模拟器 |
| 6 | yuanbao | yuanbao API | 群聊 API |
| 7 | gif-search | curl + jq + Tenor API | GIF 搜索 |
| 8 | heartmula | heartmula CLI | 歌曲生成 |
| 9 | songsee | songsee CLI | 音频分析 |
| 10 | songwriting-and-ai-music | suno API | 音乐创作 |
| 11 | youtube-content | yt-dlp | YouTube 处理 |
| 12 | zyfun-tmdb-integration | TMDB API | 电影数据库 |
| 13 | huggingface-hub | hf CLI | ML 模型管理 |
| 14 | llama-cpp | llama.cpp | 本地推理 |
| 15 | serving-llms-vllm | vLLM | 推理服务 |
| 16 | obliteratus | Python 脚本 | LLM 消融 |
| 17 | audiocraft-audio-generation | audiocraft | 音频生成 |
| 18 | segment-anything-model | SAM | 图像分割 |
| 19 | weights-and-biases | wandb CLI | 实验追踪 |
| 20 | lm-evaluation-harness | lm-eval | LLM 评估 |
| 21 | dspy | dspy | ML 编程框架 |
| 22 | jupyter-live-kernel | Jupyter | 交互式 Python |
| 23 | comfyui | ComfyUI | 生成式 AI |
| 24 | ascii-video | Python + ffmpeg | 视频处理 |
| 25 | manim-video | Manim CE | 数学动画 |
| 26 | p5js | p5.js | 创意编码 |
| 27 | pixel-art | Python 脚本 | 像素画生成 |
| 28 | excalidraw | Excalidraw | 图表绘制 |

### 🎨 Creative Skills（16 个）

| # | Skill | 输出类型 | 分类理由 |
|---|-------|---------|---------|
| 1 | architecture-diagram | SVG/HTML | 架构图生成 |
| 2 | ascii-art | 文本 | ASCII 艺术 |
| 3 | baoyu-article-illustrator | 图片 | 文章插图 |
| 4 | baoyu-comic | 图片 | 知识漫画 |
| 5 | baoyu-infographic | 图片 | 信息图 |
| 6 | claude-design | HTML | 网页原型 |
| 7 | design-md | Token Spec | 设计 Token |
| 8 | humanizer | 文本 | 去 AI 味 |
| 9 | ideation | 文本 | 创意生成 |
| 10 | popular-web-designs | HTML/CSS | 设计系统 |
| 11 | pretext | 文本 | 文本布局 |
| 12 | sketch | HTML | Mockup |
| 13 | touchdesigner-mcp | 实时视觉 | 实时视觉 |
| 14 | creative-ideation | 文本 | 创意约束 |
| 15 | ascii-video | MP4/GIF | ASCII 视频 |
| 16 | manim-video | MP4 | 数学动画 |

### 🤖 Delegate Skills（4 个）

| # | Skill | 委派目标 | 分类理由 |
|---|-------|---------|---------|
| 1 | claude-code | Claude Code CLI | 委派编码 Agent |
| 2 | codex | OpenAI Codex CLI | 委派编码 Agent |
| 3 | opencode | OpenCode CLI | 委派编码 Agent |
| 4 | kanban-codex-lane | Codex in Kanban | 委派 Kanban Agent |

### 🍎 Platform Skills（5 个）

| # | Skill | 平台 | 分类理由 |
|---|-------|------|---------|
| 1 | apple-notes | macOS | Apple Notes CLI |
| 2 | apple-reminders | macOS | Apple Reminders CLI |
| 3 | findmy | macOS | FindMy.app |
| 4 | imessage | macOS | iMessage CLI |
| 5 | macos-computer-use | macOS | macOS 屏幕操作 |

## 统计

```
类型              数量    占比      可视化
────────────────────────────────────────────
🧠 Knowledge      38     42%     ████████████████████
🔧 CLI            28     31%     ██████████████
🎨 Creative       16     18%     ████████
🤖 Delegate        4      4%     ██
🍎 Platform        5      5%     ██
🔗 MCP              1      1%     █
────────────────────────────────────────────
总计              91    100%
```

## 之前遗漏的 10 个 Skill

| Skill | 遗漏原因 |
|-------|---------|
| dogfood | 根 SKILL.md 被忽略，只算了子目录 |
| comfyui | frontmatter 解析失败 |
| weights-and-biases | 在 mlops/evaluation/ 子目录，未递归 |
| lm-evaluation-harness | 在 mlops/evaluation/ 子目录，未递归 |
| llama-cpp | 在 mlops/inference/ 子目录，未递归 |
| obliteratus | 在 mlops/inference/ 子目录，未递归 |
| serving-llms-vllm | 在 mlops/inference/ 子目录，未递归 |
| audiocraft-audio-generation | 在 mlops/models/ 子目录，未递归 |
| segment-anything-model | 在 mlops/models/ 子目录，未递归 |
| dspy | 在 mlops/research/ 子目录，未递归 |
