# 小红书笔记爬虫

基于 DrissionPage 的小红书笔记爬虫工具，支持单博主爬取、批量爬取、关键词搜索和同行监控。

## 功能特性

- **单博主爬取**：爬取指定博主的笔记，支持自定义目标数量和点赞阈值
- **批量博主爬取**：从文件读取多个博主URL，支持断点续爬
- **关键词搜索爬取**：按关键词搜索笔记，支持按最新排序
- **批量关键词爬取**：批量处理多个关键词，自动汇总去重
- **同行监控模式**：快速检查多个博主的前N篇笔记，监控爆款选题
- **反爬保护**：随机滚动、人类行为模拟、请求频率控制

## 环境要求

- Python 3.8+
- Chrome/Edge 浏览器
- 已登录的小红书账号

## 安装依赖

```bash
pip install DrissionPage openpyxl
```

## 使用说明

### 1. 单博主爬取

爬取单个博主的笔记并保存为Excel文件。

```bash
python xhs_user_spider.py
```

运行后按提示输入：
- 博主主页URL
- 目标达标笔记数量（默认50）
- 点赞数阈值（默认200）

### 2. 批量博主爬取（监控模式）

从 `resources/urls.txt` 读取博主列表，检查每个博主的前N篇笔记。

```bash
# 基本用法（检查前40篇，点赞>200）
python xhs_batch_user_spider.py

# 自定义参数
python xhs_batch_user_spider.py -c 30 -l 150

# 查看所有参数
python xhs_batch_user_spider.py --help
```

**参数说明：**
- `-f, --file`：博主URL文件路径（默认 `resources/urls.txt`）
- `-n, --num`：每个博主采集的达标笔记数量（默认50）
- `-l, --likes`：点赞数阈值（默认200）
- `-c, --check`：每个博主只检查前N篇笔记（默认40，用于监控模式）
- `--restart`：忽略进度文件，从头开始
- `--gap`：博主间间隔秒数（默认10）

### 3. 关键词搜索爬取

按关键词搜索笔记。

```bash
# 交互式输入
python xhs_keyword_spider_v2.py

# 命令行参数
python xhs_keyword_spider_v2.py -k "穿搭" -n 50 -l 200
```

**参数说明：**
- `-k, --keyword`：搜索关键词
- `-n, --num`：需要采集的达标笔记数量（默认50）
- `-l, --likes`：点赞数阈值（默认200）
- `--no-sort-time`：不按最新排序（默认按最新）

### 4. 批量关键词爬取

从 `resources/keywords.txt` 读取关键词列表，批量爬取并汇总。

```bash
# 基本用法
python xhs_batch_spider.py

# 自定义参数
python xhs_batch_spider.py -n 30 -l 150 --timeout 600

# 从头开始（忽略进度）
python xhs_batch_spider.py --restart
```

**参数说明：**
- `-f, --file`：关键词文件路径（默认 `resources/keywords.txt`）
- `-n, --num`：每个关键词采集的达标笔记数量（默认50）
- `-l, --likes`：点赞数阈值（默认200）
- `--no-sort-time`：不按最新排序
- `--restart`：忽略进度文件，从头开始
- `--timeout`：单个关键词超时秒数（默认300）

## 文件结构

```
xhs_user_mainpage/
├── xhs_user_spider.py          # 单博主爬取
├── xhs_batch_user_spider.py    # 批量博主爬取（监控模式）
├── xhs_keyword_spider_v2.py    # 关键词搜索爬取
├── xhs_batch_spider.py         # 批量关键词爬取
├── resources/
│   ├── urls.txt                # 博主URL列表（每行一个URL）
│   └── keywords.txt            # 关键词列表（每行一个关键词）
└── data/                       # 输出目录
    ├── 监控_YYYYMMDD_HHMMSS.xlsx  # 监控汇总文件
    ├── 汇总_YYYYMMDD_HHMMSS.xlsx  # 关键词汇总文件
    └── *_notes.xlsx            # 单博主/单关键词数据
```

## 配置文件

### resources/urls.txt

博主URL列表，每行一个URL，`#` 开头为注释。

```
# 同行博主URL
https://www.xiaohongshu.com/user/profile/xxx1
https://www.xiaohongshu.com/user/profile/xxx2
```

### resources/keywords.txt

关键词列表，每行一个关键词，`#` 开头为注释。

```
# 搜索关键词
穿搭
OOTD
秋季穿搭
```

## 输出说明

### 监控模式输出

- 文件名：`监控_YYYYMMDD_HHMMSS.xlsx`
- 内容：所有博主的达标笔记汇总
- 列：序号、博主、标题、点赞数、详情页URL

### 批量关键词输出

- 文件名：`汇总_YYYYMMDD_HHMMSS.xlsx`
- 内容：所有关键词的达标笔记汇总（自动去重）
- 列：序号、搜索关键词、标题、作者、类型、点赞数、详情页URL

## 反爬保护

- 随机滚动距离（300-600px）
- 随机暂停时间（1.5-3.5秒）
- 人类行为模拟（鼠标移动、悬停、小幅度滚动）
- 请求频率控制（每5次滚动休息3秒）
- 博主/关键词间间隔等待

## 注意事项

1. **必须登录**：运行前请确保浏览器已登录小红书账号
2. **控制频率**：建议不要频繁运行，避免账号被封
3. **进度保存**：批量爬取支持断点续爬，中断后下次运行自动继续
4. **数据去重**：批量关键词爬取会自动按标题去重

## 常见问题

**Q: 爬取不到数据？**
A: 检查是否已登录小红书账号，搜索接口URL是否变更。

**Q: 如何清除进度重新开始？**
A: 使用 `--restart` 参数，或删除 `data/batch_*_progress.json` 文件。

**Q: 如何调整爬取速度？**
A: 使用 `--gap` 参数调整博主间间隔，或修改代码中的随机延迟范围。
