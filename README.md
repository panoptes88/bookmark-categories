# bookmark-categories

浏览器书签分类整理工具。解析浏览器导出的 HTML 书签文件，按主题自动分类并生成新的书签文件。

## 功能特性

- 解析 Netscape 格式的浏览器书签 HTML 文件
- 按主题自动分类书签（开发/编程、DevOps/运维、AI/机器学习等）
- 支持自定义分类规则
- 生成符合浏览器导入格式的 HTML 文件
- 提供统计信息展示

## 分类类别

当前支持的分类规则：

| 分类 | 关键词示例 |
|------|-----------|
| 开发/编程 | github, leetcode, 代码, 编程, mcp |
| DevOps/运维 | docker, vps, 服务器, 监控, sre |
| 设计/创意 | 图片, 模板, nanobanana |
| AI/机器学习 | dify, llm, ai |
| 社区/资讯 | v2ex, 52pojie, 博客, 知乎 |
| 工具/导航 | shell, pingvin, hubproxy |

未匹配的书签将归入"其他"类别。

## 快速开始

### 本地运行

1. 安装依赖：

```bash
pip install beautifulsoup4
```

2. 将书签文件（HTML 格式）放到当前目录：

```bash
# 脚本会自动扫描当前目录下的所有 HTML 文件
# 识别 Netscape 格式的书签文件并进行处理
ls *.html
```

3. 运行脚本：

```bash
python parse_bookmarks.py
```

脚本会自动：
- 扫描当前目录下的所有 `.html` 文件
- 识别 Netscape 格式的书签文件
- 处理并生成 `organized_原文件名.html`

### Docker 运行

```bash
docker build -t bookmark-tool .
docker run -v $(pwd):/app bookmark-tool
```

将书签文件放到当前目录，运行后会在同目录生成整理后的文件。

## 自定义分类

编辑 `parse_bookmarks.py` 中的 `category_rules` 字典来修改分类规则：

```python
category_rules = {
    '你的分类名': ['关键词1', '关键词2'],
    # 添加更多分类...
}
```

## 输入输出

**输入格式**：浏览器导出的 Netscape Bookmark HTML 文件

**输出格式**：整理后的 Netscape Bookmark HTML 文件，可直接导入浏览器

## 依赖

- Python 3.12+
- beautifulsoup4
