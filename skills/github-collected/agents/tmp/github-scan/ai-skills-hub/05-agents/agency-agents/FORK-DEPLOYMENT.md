# 🚀 Fork 部署说明

本 Fork 用于 [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) 的自定义部署。

## 部署环境

- **服务器**: Oracle Cloud ARM (aarch64, 24GB RAM)
- **部署方式**: `convert.sh --tool opencode + install.sh`
- **注意**: `npm @opencode-ai/cli` 在 aarch64 Node 20 不可用，改用 `pip3 install opencode-cli`
- **Agent 数量**: 184 个全部部署

## 自定义修改

- 184 个 agent 人格全量部署（非精选）
- 利用 Hermes 原生 memory 系统替代 mcp-memory

## 同步

```bash
git remote add upstream https://github.com/msitarzewski/agency-agents.git
git fetch upstream
git checkout main
git merge upstream/main
```
