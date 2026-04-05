#!/usr/bin/env python3
"""
微信公众号文章读取工具

支持三种模式：
1. 直接抓取（适用于部分公开文章）
2. 浏览器自动化（需要用户先手动验证）
3. 调用 wechat-reader MCP（需预先安装）
"""

import sys
import json
import re
from pathlib import Path

# 尝试导入 playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def extract_article_from_html(html: str, url: str) -> dict:
    """从 HTML 中提取文章内容"""
    result = {
        "title": "",
        "author": "",
        "publish_time": "",
        "account": "",
        "content": "",
        "url": url,
        "status": "ok"
    }
    
    # 提取标题
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    if title_match:
        result["title"] = title_match.group(1).strip()
    
    # 提取公众号名称
    account_match = re.search(r'var accountName\s*=\s*["\']([^"\']+)["\']', html)
    if account_match:
        result["account"] = account_match.group(1).strip()
    
    # 提取作者
    author_match = re.search(r'var nickname\s*=\s*["\']([^"\']+)["\']', html)
    if author_match:
        result["author"] = author_match.group(1).strip()
    
    # 提取发布时间
    time_match = re.search(r'var createTime\s*=\s*["\']([^"\']+)["\']', html)
    if time_match:
        result["publish_time"] = time_match.group(1).strip()
    
    # 提取正文内容（微信公众号文章通常在 id="js_content" 的 div 中）
    content_match = re.search(r'id=["\']js_content["\'][^>]*>(.*?)</div>', html, re.DOTALL)
    if content_match:
        content_html = content_match.group(1)
        # 去除 HTML 标签，保留基本格式
        content_text = re.sub(r'<br\s*/?>', '\n', content_html)
        content_text = re.sub(r'<[^>]+>', '', content_text)
        # 解码 HTML 实体
        content_text = content_text.replace('&nbsp;', ' ')
        content_text = content_text.replace('&lt;', '<')
        content_text = content_text.replace('&gt;', '>')
        content_text = content_text.replace('&amp;', '&')
        content_text = content_text.replace('&quot;', '"')
        content_text = content_text.replace('&#39;', "'")
        result["content"] = content_text.strip()
    
    # 如果内容提取失败，尝试其他方式
    if not result["content"]:
        # 尝试提取所有段落
        paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
        if paragraphs:
            result["content"] = '\n\n'.join(p.strip() for p in paragraphs)
    
    return result


def read_with_browser(url: str, timeout: int = 30) -> dict:
    """使用浏览器读取文章（需要用户先手动验证）"""
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "status": "error",
            "error": "Playwright 未安装，请运行：pip install playwright"
        }
    
    try:
        with sync_playwright() as p:
            # 启动浏览器（使用现有用户数据目录，保持登录状态）
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(Path.home() / ".openclaw" / "browser" / "openclaw" / "user-data"),
                headless=False,
                channel="chrome"
            )
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            
            # 检查是否需要验证
            page_content = page.content()
            if "环境异常" in page_content or "验证" in page_content:
                return {
                    "status": "captcha_required",
                    "error": "需要用户手动验证。请在打开的浏览器窗口中完成验证，然后重新运行。",
                    "url": url
                }
            
            # 提取内容
            html = page.content()
            result = extract_article_from_html(html, url)
            
            browser.close()
            return result
            
    except PlaywrightTimeout:
        return {
            "status": "timeout",
            "error": f"页面加载超时（{timeout}秒）"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def read_with_fetch(url: str) -> dict:
    """尝试直接抓取（适用于部分公开文章）"""
    import subprocess
    
    try:
        # 使用 curl 模拟浏览器请求
        result = subprocess.run([
            "curl", "-s", "-L",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "-H", "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
            url
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            html = result.stdout
            extracted = extract_article_from_html(html, url)
            
            # 检查是否成功提取内容
            if extracted["content"]:
                return extracted
            elif "环境异常" in html or "验证" in html:
                return {
                    "status": "captcha_required",
                    "error": "需要用户手动验证"
                }
            else:
                return {
                    "status": "error",
                    "error": "无法提取文章内容，可能需要验证"
                }
        else:
            return {
                "status": "error",
                "error": f"请求失败：{result.stderr}"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "error": "请求超时"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def read_article(url: str, method: str = "auto") -> dict:
    """
    读取微信公众号文章
    
    Args:
        url: 文章链接
        method: 读取方法 ("auto" | "fetch" | "browser")
    
    Returns:
        dict: 包含文章内容的字典
    """
    # 验证 URL 格式
    if not re.match(r'https://mp\.weixin\.qq\.com/s/', url):
        return {
            "status": "error",
            "error": "无效的微信公众号文章链接"
        }
    
    if method == "auto":
        # 先尝试直接抓取
        result = read_with_fetch(url)
        if result["status"] == "ok":
            return result
        
        # 如果需要验证，提示用户使用浏览器方式
        if result["status"] == "captcha_required":
            return {
                "status": "captcha_required",
                "error": "需要用户手动验证。请使用浏览器方式：先用浏览器打开链接完成验证，然后重新运行。",
                "url": url,
                "suggestion": "在浏览器中访问该链接，完成验证后保持窗口打开，然后使用 method='browser' 重新读取"
            }
        
        # 抓取失败，尝试浏览器方式
        return read_with_browser(url)
    
    elif method == "fetch":
        return read_with_fetch(url)
    
    elif method == "browser":
        return read_with_browser(url)
    
    else:
        return {
            "status": "error",
            "error": f"未知的方法：{method}"
        }


def format_output(result: dict) -> str:
    """格式化输出结果"""
    if result["status"] != "ok":
        return f"❌ 读取失败：{result.get('error', '未知错误')}"
    
    output = []
    if result["title"]:
        output.append(f"# {result['title']}")
        output.append("")
    if result["author"]:
        output.append(f"**作者**: {result['author']}")
    if result["account"]:
        output.append(f"**公众号**: {result['account']}")
    if result["publish_time"]:
        output.append(f"**发布时间**: {result['publish_time']}")
    
    if output:
        output.append("")
        output.append("---")
        output.append("")
    
    if result["content"]:
        output.append(result["content"])
        output.append("")
    
    if result["url"]:
        output.append(f"**原文链接**: {result['url']}")
    
    return "\n".join(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python wechat_reader.py <文章链接> [method]")
        print("method: auto (默认) | fetch | browser")
        sys.exit(1)
    
    url = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    result = read_article(url, method)
    
    # 输出 JSON 格式（便于程序调用）
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 输出人类可读格式
        print(format_output(result))
