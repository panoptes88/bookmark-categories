FROM python:3.12-slim

WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir beautifulsoup4

# 复制脚本
COPY parse_bookmarks.py .

# 运行脚本
CMD ["python", "parse_bookmarks.py"]
