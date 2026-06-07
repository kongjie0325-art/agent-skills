# Zyfun 源构建实战记录 (2026-06-06)

## 仓库
- GitHub: kongjie0325-art/zyfun-sources
- 本地: /opt/data/zyfun-repo/
- 导入链接: https://raw.githubusercontent.com/kongjie0325-art/zyfun-sources/master/zyfun-sources.json

## 关键发现

### 去重策略
- 用户配置文件 229 条 site → 去重后 127 个唯一 API（71个重复）
- 同名同 API 的重复条目（如"光速资源"出现2次、"红牛资源"出现4次）
- DRPY 类型（type=7）应保留，Zyfun 支持

### URL 测试
- 用 curl 并发测试（10 workers, 8s 超时），只保留 status==200 的
- DRPY 类型（type=7, api=csp_XXX）无法 curl 测试，保留不测
- HTTP → HTTPS 自动升级
- channel 直播流可能全部来自同一推流服务器，服务器下线则全部失效需清空

### Git 推送
- 远程可能有分歧提交，先 pull --rebase
- 冲突时用 git checkout --ours 保留本地版本
- GIT_EDITOR=true 避免编辑器问题

## TMDB 集成
- API Key: 1f54bd990f1cdfb230adb312546d765d
- 用 TMDB 公开 API 获取影视元数据，封装成 Zyfun CMS JSON 格式
- 10 个分类 (热门电影/热门电视剧/科幻/动作/喜剧/剧情/悬疑/爱情/犯罪/动画)
- 详细 skill: zyfun-tmdb-integration

## 当前源统计
- 77 site (67 CMS + 10 TMDB) + 21 analyze + 8 iptv + 9 drive
- 文件 ~48KB
