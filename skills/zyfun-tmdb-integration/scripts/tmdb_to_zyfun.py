#!/usr/bin/env python3
"""
TMDB → Zyfun CMS JSON 转换器

用法:
  python3 tmdb_to_zyfun.py --api-key YOUR_KEY --type trending --media movie --output tmdb-movie-trending.json
  python3 tmdb_to_zyfun.py --api-key YOUR_KEY --type genre --genre-id 878 --media movie --output tmdb-movie-科幻.json
  python3 tmdb_to_zyfun.py --api-key YOUR_KEY --type discover --genre-id 28 --media movie --output tmdb-movie-动作.json

依赖: 纯标准库 (urllib, json, argparse)
"""
import json, urllib.request, urllib.error, urllib.parse, argparse, time, sys

TMDB_BASE = "https://api.themoviedb.org/3"

def api_get(url, retries=2):
    """GET TMDB API with retry"""
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if i < retries:
                time.sleep(1)
            else:
                print(f"  ⚠️ API 请求失败: {url[:80]}... ({str(e)[:50]})", file=sys.stderr)
                return None

def tmdb_search(query, type, api_key):
    encoded = urllib.parse.quote(query)
    url = f"{TMDB_BASE}/search/{type}?api_key={api_key}&language=zh-CN&query={encoded}&page=1"
    return api_get(url) or {"results": []}

def tmdb_detail(tmdb_id, type, api_key):
    url = f"{TMDB_BASE}/{type}/{tmdb_id}?api_key={api_key}&language=zh-CN&append_to_response=credits"
    return api_get(url)

def tmdb_trending(type, api_key):
    url = f"{TMDB_BASE}/trending/{type}/week?api_key={api_key}&language=zh-CN"
    return api_get(url) or {"results": []}

def tmdb_discover(genre_id, type, api_key):
    url = f"{TMDB_BASE}/discover/{type}?api_key={api_key}&language=zh-CN&with_genres={genre_id}&sort_by=popularity.desc&page=1"
    return api_get(url) or {"results": []}

def convert_movie(movie, detail=None):
    actors = []
    genres_str = ""
    director = ""
    if detail:
        actors = [c["name"] for c in detail.get("credits", {}).get("cast", [])[:3]]
        for c in detail.get("credits", {}).get("crew", []):
            if c.get("job") == "Director":
                director = c["name"]
                break
        genres_str = ", ".join(g["name"] for g in detail.get("genres", []))

    poster = movie.get("poster_path") or ""
    return {
        "vod_id": f"tmdb_m_{movie['id']}",
        "vod_name": movie.get("title", ""),
        "type_id": 1,
        "type_name": "电影",
        "vod_en": movie.get("original_title", movie.get("title", "")),
        "vod_time": movie.get("release_date", ""),
        "vod_remarks": f"⭐{movie.get('vote_average',0)} | {genres_str} | {', '.join(actors)}",
        "vod_class": "tmdb",
        "vod_actor": ", ".join(actors),
        "vod_director": director,
        "vod_content": movie.get("overview", ""),
        "vod_pic": f"https://image.tmdb.org/t/p/w500{poster}" if poster else "",
    }

def convert_tv(tv, detail=None):
    actors = []
    genres_str = ""
    if detail:
        actors = [c["name"] for c in detail.get("credits", {}).get("cast", [])[:3]]
        genres_str = ", ".join(g["name"] for g in detail.get("genres", []))

    seasons = detail.get("number_of_seasons", 0) if detail else 0
    episodes = detail.get("number_of_episodes", 0) if detail else 0
    poster = tv.get("poster_path") or ""
    return {
        "vod_id": f"tmdb_t_{tv['id']}",
        "vod_name": tv.get("name", ""),
        "type_id": 2,
        "type_name": "电视剧",
        "vod_en": tv.get("original_name", tv.get("name", "")),
        "vod_time": tv.get("first_air_date", ""),
        "vod_remarks": f"⭐{tv.get('vote_average',0)} | {genres_str} | {', '.join(actors)} | {seasons}季 {episodes}集",
        "vod_class": "tmdb",
        "vod_actor": ", ".join(actors),
        "vod_content": tv.get("overview", ""),
        "vod_pic": f"https://image.tmdb.org/t/p/w500{poster}" if poster else "",
    }

def main():
    parser = argparse.ArgumentParser(description="TMDB → Zyfun CMS JSON 转换器")
    parser.add_argument("--api-key", required=True, help="TMDB API Key")
    parser.add_argument("--type", required=True, choices=["trending", "genre", "search"], help="数据类型")
    parser.add_argument("--media", default="movie", choices=["movie", "tv"], help="媒体类型")
    parser.add_argument("--genre-id", help="类型 ID (genre 模式必需)")
    parser.add_argument("--query", help="搜索关键词 (search 模式必需)")
    parser.add_argument("--limit", type=int, default=20, help="返回数量")
    parser.add_argument("--detail", action="store_true", help="获取详细信息（演员/类型/导演），会触发额外 API 调用")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    results = []

    if args.type == "trending":
        data = tmdb_trending(args.media, args.api_key)
        items = data.get("results", [])[:args.limit]
        for item in items:
            detail = None
            if args.detail:
                detail = tmdb_detail(item["id"], args.media, args.api_key)
            if args.media == "movie":
                results.append(convert_movie(item, detail))
            else:
                results.append(convert_tv(item, detail))

    elif args.type == "genre":
        if not args.genre_id:
            print("❌ genre 模式需要 --genre-id 参数", file=sys.stderr)
            sys.exit(1)
        data = tmdb_discover(args.genre_id, args.media, args.api_key)
        items = data.get("results", [])[:args.limit]
        for item in items:
            detail = None
            if args.detail:
                detail = tmdb_detail(item["id"], args.media, args.api_key)
            if args.media == "movie":
                results.append(convert_movie(item, detail))
            else:
                results.append(convert_tv(item, detail))

    elif args.type == "search":
        if not args.query:
            print("❌ search 模式需要 --query 参数", file=sys.stderr)
            sys.exit(1)
        data = tmdb_search(args.query, args.media, args.api_key)
        items = data.get("results", [])[:args.limit]
        for item in items:
            detail = None
            if args.detail:
                detail = tmdb_detail(item["id"], args.media, args.api_key)
            if args.media == "movie":
                results.append(convert_movie(item, detail))
            else:
                results.append(convert_tv(item, detail))

    output = {
        "code": 1, "msg": "数据列表", "page": 1, "pagecount": 1,
        "limit": str(args.limit), "total": len(results), "list": results
    }
    with open(args.output, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"✅ 生成 {args.output}: {len(results)} 条 {'电影' if args.media == 'movie' else '电视剧'}")

if __name__ == "__main__":
    main()
