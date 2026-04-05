#!/usr/bin/env python3
"""
OpenClaw Tool - 微信公众号文章读取

使用方法：
python tool.py <文章链接>

输出：格式化后的文章内容（Markdown 格式）
"""

import sys
import json
from pathlib import Path

# 导入核心读取模块
sys.path.insert(0, str(Path(__file__).parent))
from wechat_reader import read_article, format_output


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "error": "缺少参数：文章链接",
            "usage": "python tool.py <文章链接>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 验证 URL 格式
    if not url.startswith("https://mp.weixin.qq.com/s/"):
        print(json.dumps({
            "status": "error",
            "error": "无效的微信公众号文章链接",
            "expected_format": "https://mp.weixin.qq.com/s/xxxxx"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 读取文章
    result = read_article(url, method="auto")
    
    # 输出结果
    if result["status"] == "ok":
        # 成功：输出格式化内容
        output = format_output(result)
        print(output)
    else:
        # 失败：输出错误信息
        error_msg = f"❌ 读取失败：{result.get('error', '未知错误')}"
        if result.get("suggestion"):
            error_msg += f"\n\n💡 建议：{result['suggestion']}"
        print(error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
