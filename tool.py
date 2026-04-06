#!/usr/bin/env python3
"""
OpenClaw Tool - 微信公众号文章读取（优化版）

使用方法：
python tool.py <文章链接> [auto|fetch|browser] [--json] [--quiet]

参数：
- auto: 自动模式（默认），先尝试直接抓取，失败则用浏览器
- fetch: 仅直接抓取
- browser: 仅浏览器模式
- --json: 输出 JSON 格式
- --quiet: 静默模式，不显示进度信息

输出：格式化后的文章内容（Markdown 格式）
"""

import sys
import json
from pathlib import Path

# 导入核心读取模块
sys.path.insert(0, str(Path(__file__).parent))
from wechat_reader import read_article, format_output


def print_usage():
    """打印使用说明"""
    print("""
📰 微信公众号文章读取工具

用法：
  python tool.py <文章链接> [模式] [选项]

模式（可选，默认 auto）：
  auto     自动模式：先直接抓取，失败则用浏览器（推荐）
  fetch    仅直接抓取：速度快，但部分文章需要验证
  browser  仅浏览器：适用于需要验证的文章

选项：
  --json   输出 JSON 格式（便于程序处理）
  --quiet  静默模式：不显示进度信息
  --help   显示此帮助信息

示例：
  python tool.py "https://mp.weixin.qq.com/s/xxxxx"
  python tool.py "https://mp.weixin.qq.com/s/xxxxx" browser --json
  python tool.py "https://mp.weixin.qq.com/s/xxxxx" fetch --quiet
""")


def main():
    # 解析参数
    args = sys.argv[1:]
    
    if not args or "--help" in args or "-h" in args:
        print_usage()
        sys.exit(0)
    
    # 提取选项
    url = None
    method = "auto"
    output_json = False
    verbose = True
    
    for arg in args:
        if arg == "--json":
            output_json = True
        elif arg == "--quiet":
            verbose = False
        elif arg in ["auto", "fetch", "browser"]:
            method = arg
        elif not arg.startswith("-"):
            url = arg
    
    if not url:
        if output_json:
            print(json.dumps({
                "status": "error",
                "error": "缺少参数：文章链接",
                "usage": "python tool.py <文章链接> [auto|fetch|browser] [--json] [--quiet]"
            }, ensure_ascii=False, indent=2))
        else:
            print("❌ 错误：缺少文章链接")
            print_usage()
        sys.exit(1)
    
    # 读取文章
    result = read_article(url, method=method, verbose=verbose)
    
    # 输出结果
    if output_json:
        # JSON 格式输出
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 人类可读格式
        if result["status"] == "ok":
            output = format_output(result)
            print(output)
        else:
            # 失败：输出错误信息和建议
            error_msg = f"❌ 读取失败：{result.get('error', '未知错误')}"
            if result.get("suggestion"):
                error_msg += f"\n\n💡 建议：{result['suggestion']}"
            if result.get("details"):
                error_msg += f"\n\n📝 说明：{result['details']}"
            print(error_msg, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
