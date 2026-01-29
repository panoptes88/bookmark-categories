#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析浏览器书签HTML文件，分析并整理书签内容
"""

import re
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup


def parse_bookmarks(file_path):
    """解析书签HTML文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    bookmarks = []
    current_folder = "根目录"

    # 查找所有 DT 标签（包含书签和文件夹）
    for dt in soup.find_all('dt'):
        # 处理文件夹
        h3 = dt.find('h3')
        if h3:
            folder_name = h3.get_text()
            current_folder = folder_name
            continue

        # 处理书签
        a_tag = dt.find('a')
        if a_tag:
            href = a_tag.get('href', '')
            title = a_tag.get_text(strip=True)
            add_date = a_tag.get('add_date', '')
            icon = a_tag.get('icon', '')

            if add_date:
                try:
                    add_date = datetime.datetime.fromtimestamp(int(add_date))
                except:
                    add_date = None
            else:
                add_date = None

            bookmarks.append({
                'title': title,
                'url': href,
                'folder': current_folder,
                'add_date': add_date,
                'icon': icon
            })

    return bookmarks


def categorize_bookmarks(bookmarks):
    """根据主题对书签进行分类"""
    categories = defaultdict(list)

    # 定义分类规则
    category_rules = {
        '开发/编程': ['github.com', 'gitstar-ranking.com', 'leetcode', '代码', '编程', '开发', 'dev', 'mcp', 'pake'],
        'DevOps/运维': ['sre-platform', 'opsnote', 'docker', 'vps', '服务器', '监控', '网络', '拨测', '海底光缆'],
        '设计/创意': ['模板码', '图片制作', 'postimages', 'create.wan.video', 'nanobanana', '图片'],
        'AI/机器学习': ['dify', '***REMOVED***', 'sherpa-onnx', 'llmcodearena', 'nano-banana'],
        '社区/资讯': ['v2ex.com', '52pojie', '博客', '知乎', '微信公众号', 'linux.do'],
        '工具/导航': ['ishell', 'yourls', 'pingvin-share', 'hubproxy', 'kspeeder']
    }

    for bookmark in bookmarks:
        categorized = False

        # 根据URL和标题匹配分类
        for category, keywords in category_rules.items():
            url = bookmark['url'].lower()
            title = bookmark['title'].lower()

            for keyword in keywords:
                if keyword.lower() in url or keyword.lower() in title:
                    categories[category].append(bookmark)
                    categorized = True
                    break

            if categorized:
                break

        # 未匹配到分类的默认分到其他
        if not categorized:
            categories['其他'].append(bookmark)

    return categories


def generate_html(bookmarks, categories, output_path):
    """生成新的HTML文件"""
    # 创建HTML结构
    html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>整理后的书签</TITLE>
<H1>整理后的书签</H1>
<DL><p>
"""

    # 添加分类文件夹
    for category in sorted(categories.keys()):
        folder_html = f'    <DT><H3>{category}</H3>\n'
        folder_html += '    <DL><p>\n'

        for bookmark in sorted(categories[category], key=lambda x: x['title']):
            title = bookmark['title']
            url = bookmark['url']
            add_date = ''
            if bookmark['add_date']:
                add_date = f' ADD_DATE="{int(bookmark["add_date"].timestamp())}"'
            icon = ''
            if bookmark['icon']:
                icon = f' ICON="{bookmark["icon"]}"'
            folder_html += f'        <DT><A HREF="{url}"{add_date}{icon}>{title}</A>\n'

        folder_html += '    </DL><p>\n'
        html_content += folder_html

    html_content += '</DL><p>\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"整理后的书签已保存到: {output_path}")


def print_statistics(bookmarks, categories):
    """打印统计信息"""
    print(f"总书签数量: {len(bookmarks)}")
    print(f"分类数量: {len(categories)}")
    print("\n分类分布:")
    for category in sorted(categories.keys()):
        print(f"  {category}: {len(categories[category])} 个")


def main():
    input_file = '/app/favorites_2026_1_29.html'
    output_file = '/app/bookmarks_organized.html'

    # 解析书签
    bookmarks = parse_bookmarks(input_file)

    # 分类
    categories = categorize_bookmarks(bookmarks)

    # 打印统计信息
    print_statistics(bookmarks, categories)

    # 生成新的HTML文件
    generate_html(bookmarks, categories, output_file)


if __name__ == "__main__":
    main()
