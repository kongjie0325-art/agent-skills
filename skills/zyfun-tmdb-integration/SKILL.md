---
name: zyfun-tmdb-integration
description: Integrate TMDB (The Movie Database) API as a Zyfun video source — wrap TMDB metadata into Zyfun CMS JSON format for catalog browsing with CMS-backed playback.
metadata:
  version: "1.0"
  triggers:
    - "TMDB"
    - "影视数据库"
    - "电影分类"
    - "电视剧分类"
    - "metadata source"
    - "Zyfun TMDB"
---

# TMDB → Zyfun 元数据源集成

> TMDB (The Movie Database) 提供免费公开 API，可获取影视元数据（标题、简介、评分、封面、演员、类型）。将这些数据封装成 Zyfun 标准的 CMS JSON 格式，用户可通过 TMDB 分类浏览热门影视，点击后在已有 CMS 资源站中搜索匹配播放。

## 核心思路

1. **TMDB API** 提供免费、无需认证的影视元数据（搜索、详情、热门、按类型浏览）
2. **Zyfun** 使用标准 CMS JSON 格式（`vod_id`, `vod_name`, `vod_remarks`, `vod_content` 等字段）
3. **桥接**：将 TMDB API 响应转换为 Zyfun CMS JSON 文件，托管在 GitHub，作为 Zyfun 的 site 源导入
4. **播放**：TMDB 只提供元数据，播放地址由 Zyfun 在已有的 CMS 资源站中搜索匹配

## TMDB API 参考

- API Key (公开免费): 注册 TMDB 账号后获取
- Base URL: `https://api.themoviedb.org/3`
- 语言参数: `language=zh-CN` (返回中文数据)

### 关键端点

```
# 搜索
GET /search/movie?api_key=KEY&language=zh-CN&query=关键词&page=1
GET /search/tv?api_key=KEY&language=zh-CN&query=关键词&page=1

# 详情 (含演员)
GET /movie/{id}?api_key=KEY&language=zh-CN&append_to_response=credits
GET /tv/{id}?api_key=KEY&language=zh-CN&append_to_response=credits

# 热门 (每周趋势)
GET /trending/movie/week?api_key=KEY&language=zh-CN
GET /trending/tv/week?api_key=KEY&language=zh-CN

# 按类型发现
GET /discover/movie?api_key=KEY&language=zh-CN&with_genres=878&sort_by=popularity.desc

# 类型列表
GET /genre/movie/list?api_key=KEY&language=zh-CN
```

### 类型 ID 映射

| 类型 | ID |
|------|-----|
| 动作 | 28 |
| 冒险 | 12 |
| 动画 | 16 |
| 喜剧 | 35 |
| 犯罪 | 80 |
| 纪录 | 99 |
| 剧情 | 18 |
| 家庭 | 10751 |
| 奇幻 | 14 |
| 历史 | 36 |
| 恐怖 | 27 |
| 音乐 | 10402 |
| 悬疑 | 9648 |
| 爱情 | 10749 |
| 科幻 | 878 |
| 惊悚 | 53 |
| 战争 | 10752 |
| 西部 | 37 |

## Zyfun CMS JSON 格式

TMDB 数据需转换为以下格式（Zyfun 标准 CMS 响应）：

```json
{
  "code": 1,
  "msg": "数据列表",
  "page": 1,
  "pagecount": 1,
  "limit": "20",
  "total": 20,
  "list": [
    {
      "vod_id": "tmdb_m_12345",
      "vod_name": "电影标题",
      "type_id": 1,
      "type_name": "电影",
      "vod_en": "Original Title",
      "vod_time": "2024-01-01",
      "vod_remarks": "⭐8.5 | 科幻, 动作 | 演员1, 演员2",
      "vod_class": "tmdb",
      "vod_actor": "演员1, 演员2",
      "vod_director": "导演",
      "vod_content": "简介...",
      "vod_pic": "https://image.tmdb.org/t/p/w500/poster_path.jpg"
    }
  ]
}
```

### 字段映射

| Zyfun 字段 | TMDB 来源 |
|-----------|-----------|
| `vod_id` | `tmdb_m_{id}` 或 `tmdb_t_{id}` (加前缀区分) |
| `vod_name` | `title` (电影) / `name` (电视剧) |
| `type_id` | 1=电影, 2=电视剧 |
| `vod_en` | `original_title` / `original_name` |
| `vod_time` | `release_date` / `first_air_date` |
| `vod_remarks` | `⭐{vote_average} | {genres} | {actors}` |
| `vod_actor` | `credits.cast[0:3]` 取 name |
| `vod_director` | `credits.crew` 中 job=Director |
| `vod_content` | `overview` |
| `vod_pic` | `https://image.tmdb.org/t/p/w500{poster_path}` |

## 生成流程

### 1. 获取数据

```python
import urllib.request, json, urllib.parse

TMDB_KEY = "your_api_key"
BASE = "https://api.themoviedb.org/3"

def tmdb_search(query, type="movie"):
    encoded = urllib.parse.quote(query)
    url = f"{BASE}/search/{type}?api_key={TMDB_KEY}&language=zh-CN&query={encoded}&page=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read().decode('utf-8'))

def tmdb_trending(type="movie"):
    url = f"{BASE}/trending/{type}/week?api_key={TMDB_KEY}&language=zh-CN"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read().decode('utf-8'))


def tmdb_discover(genre_id, type="movie"):
    url = f"{BASE}/discover/{type}?api_key={TMDB_KEY}&language=zh-CN&with_genres={genre_id}&sort_by=popularity.desc"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read().decode('utf-8'))
```

### 2. 转换并保存

```python
def convert_movie(movie, detail=None):
    """将 TMDB 电影对象转换为 Zyfun CMS 格式"""
    actors = []
    genres_str = ""
    if detail:
        actors = [c["name"] for c in detail.get("credits", {}).get("cast", [])[:3]]
        genres_str = ", ".join(g["name"] for g in detail.get("genres", []))
    
    return {
        "vod_id": f"tmdb_m_{movie['id']}",
        "vod_name": movie["title"],
        "type_id": 1,
        "type_name": "电影",
        "vod_en": movie.get("original_title", movie["title"]),
        "vod_time": movie.get("release_date", ""),
        "vod_remarks": f"⭐{movie.get('vote_average',0)} | {genres_str} | {', '.join(actors)}",
        "vod_class": "tmdb",
        "vod_actor": ", ".join(actors),
        "vod_content": movie.get("overview", ""),
        "vod_pic": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "",
    }


# 获取热门电影
trending = tmdb_trending("movie")
movie_list = []
for r in trending.get("results", [])[:20]:
    try:
        detail = tmdb_detail(r["id"], "movie")
        movie_list.append(convert_movie(r, detail))
    except:
        movie_list.append(convert_movie(r))

# 保存为 Zyfun CMS JSON
output = {
    "code": 1, "msg": "数据列表", "page": 1, "pagecount": 1,
    "limit": "20", "total": len(movie_list), "list": movie_list
}
with open("tmdb-movie-trending.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
```

### 3. 添加为 Zyfun site

在 `zyfun-sources.json` 的 `site[]` 中添加：

```json
{
  "id": "uuid",
  "key": "uuid-without-dashes",
  "name": "🔥 TMDB-热门电影",
  "api": "https://raw.githubusercontent.com/OWNER/REPO/master/tmdb-movie-trending.json",
  "playUrl": "",
  "search": false,
  "group": "影视",
  "type": 1,
  "ext": "",
  "categories": "tmdb",
  "isActive": true,
  "createdAt": 1717700000000,
  "updatedAt": 1717700000000
}
```

## 分类策略

建议生成以下 TMDB site（每个对应一个 JSON 文件）：

| Site 名称 | 数据来源 | 数量 |
|-----------|---------|------|
| 🔥 TMDB-热门电影 | `/trending/movie/week` | 20-30 |
| 🔥 TMDB-热门电视剧 | `/trending/tv/week` | 20-30 |
| 🎬 TMDB-科幻 | `/discover?with_genres=878` | 10-20 |
| 🎬 TMDB-动作 | `/discover?with_genres=28` | 10-20 |
| 🎬 TMDB-喜剧 | `/discover?with_genres=35` | 10-20 |
| 🎬 TMDB-剧情 | `/discover?with_genres=18` | 10-20 |
| 🎬 TMDB-悬疑 | `/discover?with_genres=9648` | 10-20 |
| 🎬 TMDB-爱情 | `/discover?with_genres=10749` | 10-20 |
| 🎬 TMDB-犯罪 | `/discover?with_genres=80` | 10-20 |
| 🎬 TMDB-动画 | `/discover?with_genres=16` | 10-20 |

## 脚本

`scripts/tmdb_to_zyfun.py` — 完整的命令行工具，支持 trending/genre/search 三种模式：

```bash
# 生成热门电影
python3 scripts/tmdb_to_zyfun.py --api-key KEY --type trending --media movie --limit 20 --detail --output tmdb-movie-trending.json

# 生成科幻电影
python3 scripts/tmdb_to_zyfun.py --api-key KEY --type genre --genre-id 878 --media movie --limit 10 --detail --output tmdb-movie-科幻.json

# 搜索
python3 scripts/tmdb_to_zyfun.py --api-key KEY --type search --query "狂飙" --media tv --limit 10 --detail --output tmdb-search-狂飙.json
```

依赖：纯标准库（urllib, json, argparse），无需 pip install。

## 注意

- TMDB API 有速率限制（约 40 次/10秒），批量获取详情时注意间隔
- `trending/week` 每周更新一次，建议定期刷新 JSON 文件
- TMDB 只提供元数据，**播放依赖已有 CMS 资源站的搜索结果**
- 封面图使用 `https://image.tmdb.org/t/p/w500{poster_path}` (w500 宽度)
- 原始封面 `original` 分辨率可能过高，建议用 `w500` 或 `w780`
