# Zyfun/TVBox 远端导入 JSON 格式

## 标准数据库导出结构 (v3.4.1+)

远端导入需要标准 JSON 格式，包含五大顶层数组：

```json
{
  "analyze": [...],
  "site": [...],
  "iptv": [...],
  "drive": [...],
  "setting": [...]
}
```

## 各数组字段要求

### site[] (CMS 资源站)
```json
{
  "id": "uuid",
  "key": "uuid-without-dashes",
  "name": "资源站名称",
  "api": "https://api.example.com/api.php/provide/vod/",
  "playUrl": "",
  "search": true,
  "group": "默认",
  "type": 1,
  "ext": "",
  "categories": "",
  "isActive": true,
  "createdAt": 1717700000000,
  "updatedAt": 1717700000000
}
```

**type 值**: 0=XML, 1=JSON, 7=DRPY, 13=Alist
**search**: true=支持搜索, false=仅列表
**group**: 分类名称（默认/切片/tvbox/API/DRPY/官采/app/影视/4K/云盘/NaFei）

### analyze[] (解析接口)
```json
{
  "id": "uuid",
  "key": "uuid-without-dashes",
  "name": "解析名称",
  "api": "https://jx.example.com/?url=",
  "type": 2,
  "flag": [],
  "headers": {},
  "script": "",
  "isActive": true,
  "createdAt": 1717700000000,
  "updatedAt": 1717700000000
}
```

### iptv[] (直播源)
```json
{
  "id": "uuid",
  "key": "uuid-without-dashes",
  "name": "直播名称",
  "api": "https://example.com/stream.m3u",
  "type": 1,
  "epg": "https://epg.example.com/?ch={name}&date={date}",
  "logo": "https://example.com/logo/{name}.png",
  "headers": {},
  "isActive": true,
  "createdAt": 1717700000000,
  "updatedAt": 1717700000000
}
```

### drive[] (云盘)
```json
{
  "id": "uuid",
  "key": "uuid-without-dashes",
  "name": "云盘名称",
  "server": "https://alist.example.com",
  "showAll": false,
  "startPage": "",
  "search": false,
  "headers": "{}",
  "params": "{}",
  "isActive": true
}
```

### setting[]
```json
{
  "version": "3.4.4",
  "disclaimer": "",
  "theme": "dark",
  "lang": "zh-CN",
  "timeout": 10
}
```

## 导入方式
Zyfun → 设置 → 基础配置 → 数据管理 → 数据导入 → 远端导入 → 粘贴 URL

## 注意事项
- 不支持自定义 categories 格式（旧版 TVBox 格式）
- 每个条目必须有 id 和 key（UUID 格式）
- isActive 必须为 true
- createdAt/updatedAt 为毫秒时间戳
- HTTP 链接会自动升级为 HTTPS
