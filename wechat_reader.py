#!/usr/bin/env python3
"""
微信公众号文章读取工具（优化版）

支持三种模式：
1. 直接抓取（适用于部分公开文章）
2. 浏览器自动化（需要用户先手动验证）
3. 调用 wechat-reader MCP（需预先安装）

优化点：
- 进度提示
- 错误分类和清晰引导
- 改进的内容提取（保留图片、格式）
- 自动重试机制
"""

import sys
import json
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any

# 尝试导入 playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


# ============= 配置 =============
DEFAULT_TIMEOUT = 30  # 默认超时时间（秒）
MAX_RETRIES = 2  # 最大重试次数
RETRY_DELAY = 1  # 重试间隔（秒）


def extract_article_from_html(html: str, url: str) -> dict:
    """
    从 HTML 中提取文章内容（优化版）
    
    改进：
    - 保留图片为 Markdown 格式
    - 保留粗体、斜体等格式
    - 保留链接
    - 更好的段落识别
    """
    result = {
        "title": "",
        "author": "",
        "publish_time": "",
        "account": "",
        "content": "",
        "url": url,
        "status": "ok",
        "images": [],
        "links": []
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
    content_match = re.search(r'id=["\']js_content["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if content_match:
        content_html = content_match.group(1)
        result["content"] = convert_html_to_markdown(content_html, result)
    
    # 如果内容提取失败，尝试其他方式
    if not result["content"].strip():
        # 尝试提取所有段落
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        if paragraphs:
            para_texts = []
            for p in paragraphs:
                text = convert_html_to_markdown(p, result)
                if text.strip():
                    para_texts.append(text.strip())
            result["content"] = '\n\n'.join(para_texts)
    
    return result


def convert_html_to_markdown(html: str, result: dict) -> str:
    """
    将 HTML 转换为 Markdown 格式
    
    保留：
    - 图片：![alt](src)
    - 链接：[text](url)
    - 粗体：**text**
    - 斜体：*text*
    - 换行：保留
    """
    text = html
    
    # 1. 处理图片 <img src="..." alt="...">
    def replace_img(match):
        src = match.group(1) or match.group(3)
        alt = match.group(2) or '图片'
        # 如果是 base64 或 data URI，跳过
        if src.startswith('data:'):
            return ''
        result["images"].append(src)
        return f'![{alt}]({src})'
    
    text = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'](?:[^>]*alt=["\']([^"\']*)["\'])?[^>]*>', replace_img, text, flags=re.IGNORECASE)
    text = re.sub(r'<img[^>]*alt=["\']([^"\']*)["\'](?:[^>]*src=["\']([^"\']+)["\'])?[^>]*>', replace_img, text, flags=re.IGNORECASE)
    
    # 2. 处理链接 <a href="...">text</a>
    def replace_link(match):
        href = match.group(1)
        link_text = match.group(2)
        # 过滤 javascript: 链接
        if href.startswith('javascript:'):
            return link_text
        result["links"].append(href)
        return f'[{link_text}]({href})'
    
    text = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', replace_link, text, flags=re.IGNORECASE)
    
    # 3. 处理粗体 <strong> 或 <b>
    text = re.sub(r'<(?:strong|b)[^>]*>([^<]+)</(?:strong|b)>', r'**\1**', text, flags=re.IGNORECASE)
    
    # 4. 处理斜体 <em> 或 <i>
    text = re.sub(r'<(?:em|i)[^>]*>([^<]+)</(?:em|i)>', r'*\1*', text, flags=re.IGNORECASE)
    
    # 5. 处理换行 <br>
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 6. 处理段落 <p>
    text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<p[^>]*>', '', text, flags=re.IGNORECASE)
    
    # 7. 去除所有剩余 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 8. 解码 HTML 实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&mdash;', '—')
    text = text.replace('&hellip;', '…')
    
    # 9. 清理空白
    text = re.sub(r'\n\s*\n', '\n\n', text)  # 多个空行合并为一个
    text = text.strip()
    
    return text


def print_progress(message: str, verbose: bool = True):
    """打印进度信息"""
    if verbose:
        print(f"🔄 {message}", file=sys.stderr)


def read_with_browser(url: str, timeout: int = DEFAULT_TIMEOUT, verbose: bool = True) -> dict:
    """
    使用浏览器读取文章（需要用户先手动验证）
    
    改进：
    - 进度提示
    - 更清晰的验证引导
    - 错误分类
    """
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "status": "error",
            "error": "Playwright 未安装",
            "suggestion": "请运行：pip install playwright && playwright install chromium"
        }
    
    print_progress("正在启动浏览器...", verbose)
    
    try:
        with sync_playwright() as p:
            # 启动浏览器（使用现有用户数据目录，保持登录状态）
            user_data_dir = str(Path.home() / ".openclaw" / "browser" / "openclaw" / "user-data")
            
            try:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=False,  # 必须可见，以便用户完成验证
                    channel="chrome",
                    timeout=timeout * 1000
                )
                print_progress("浏览器已启动 ✓", verbose)
            except Exception as e:
                # 如果 Chrome 不可用，尝试 Chromium
                print_progress("Chrome 不可用，尝试 Chromium...", verbose)
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=False,
                    timeout=timeout * 1000
                )
                print_progress("Chromium 已启动 ✓", verbose)
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            print_progress(f"正在访问文章链接...", verbose)
            try:
                page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
                print_progress("页面已加载 ✓", verbose)
            except PlaywrightTimeout:
                return {
                    "status": "timeout",
                    "error": f"页面加载超时（{timeout}秒）",
                    "suggestion": "请检查网络连接，或尝试增加超时时间"
                }
            
            # 等待内容加载
            time.sleep(2)  # 给页面一些时间渲染
            
            # 检查是否需要验证
            page_content = page.content()
            
            if "环境异常" in page_content or "验证" in page_content or "安全验证" in page_content:
                print_progress("⚠️  需要验证", verbose)
                return {
                    "status": "captcha_required",
                    "error": "需要用户手动验证",
                    "suggestion": "请在打开的浏览器窗口中完成验证（滑块或扫码），验证后关闭窗口并重新运行。验证后会话将保持约 24 小时。",
                    "url": url,
                    "details": "微信检测到异常访问，需要完成安全验证。这是正常现象，验证一次后可多次使用。"
                }
            
            # 检查是否访问了不存在的文章
            if "页面不存在" in page_content or "该内容已被发布者删除":
                return {
                    "status": "not_found",
                    "error": "文章不存在或已被删除",
                    "suggestion": "文章可能已被发布者删除，或链接有误"
                }
            
            # 提取内容
            print_progress("正在提取文章内容...", verbose)
            html = page.content()
            result = extract_article_from_html(html, url)
            
            # 检查是否成功提取内容
            if not result["content"].strip():
                return {
                    "status": "extract_failed",
                    "error": "无法提取文章内容",
                    "suggestion": "文章可能需要验证，或使用了特殊的排版格式",
                    "title": result["title"]  # 至少返回标题
                }
            
            print_progress(f"文章提取成功 ✓ (标题：{result['title'][:30]}...)", verbose)
            
            browser.close()
            return result
            
    except Exception as e:
        error_msg = str(e)
        if "Target page, context or browser has been closed" in error_msg:
            return {
                "status": "error",
                "error": "浏览器窗口被意外关闭",
                "suggestion": "请保持浏览器窗口打开直到提取完成"
            }
        elif "net::ERR_CONNECTION" in error_msg or "net::ERR_NAME_NOT_RESOLVED" in error_msg:
            return {
                "status": "network_error",
                "error": "网络连接失败",
                "suggestion": "请检查网络连接后重试"
            }
        else:
            return {
                "status": "error",
                "error": f"浏览器错误：{error_msg}",
                "suggestion": "如问题持续，请尝试先用浏览器手动访问链接完成验证"
            }


def read_with_fetch(url: str, timeout: int = DEFAULT_TIMEOUT, verbose: bool = True) -> dict:
    """
    尝试直接抓取（适用于部分公开文章）
    
    改进：
    - 自动重试机制
    - 更好的错误分类
    - 进度提示
    """
    import subprocess
    
    print_progress("正在尝试直接抓取...", verbose)
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # 使用 curl 模拟浏览器请求
            result = subprocess.run([
                "curl", "-s", "-L",
                "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "-H", "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
                "--connect-timeout", str(timeout),
                "--max-time", str(timeout * 2),
                url
            ], capture_output=True, text=True, timeout=timeout * 2)
            
            if result.returncode == 0:
                html = result.stdout
                extracted = extract_article_from_html(html, url)
                
                # 检查是否成功提取内容
                if extracted["content"].strip():
                    print_progress(f"直接抓取成功 ✓ (标题：{extracted['title'][:30]}...)", verbose)
                    return extracted
                elif "环境异常" in html or "验证" in html or "安全验证" in html:
                    print_progress("⚠️  需要验证", verbose)
                    return {
                        "status": "captcha_required",
                        "error": "需要用户手动验证",
                        "suggestion": "请先用浏览器访问链接完成验证，然后重新运行",
                        "url": url
                    }
                elif "页面不存在" in html or "该内容已被发布者删除" in html:
                    return {
                        "status": "not_found",
                        "error": "文章不存在或已被删除",
                        "suggestion": "文章可能已被发布者删除，或链接有误"
                    }
                else:
                    # 抓取到了内容但无法提取，可能是格式特殊
                    if attempt < MAX_RETRIES:
                        print_progress(f"提取失败，重试 {attempt + 1}/{MAX_RETRIES}...", verbose)
                        time.sleep(RETRY_DELAY)
                        continue
                    return {
                        "status": "extract_failed",
                        "error": "无法提取文章内容",
                        "suggestion": "文章可能使用了特殊格式，请尝试浏览器模式",
                        "title": extracted["title"]
                    }
            else:
                error_stderr = result.stderr
                if attempt < MAX_RETRIES:
                    print_progress(f"请求失败，重试 {attempt + 1}/{MAX_RETRIES}...", verbose)
                    time.sleep(RETRY_DELAY)
                    continue
                return {
                    "status": "network_error",
                    "error": f"请求失败：{error_stderr[:100]}",
                    "suggestion": "请检查网络连接后重试"
                }
                
        except subprocess.TimeoutExpired:
            if attempt < MAX_RETRIES:
                print_progress(f"请求超时，重试 {attempt + 1}/{MAX_RETRIES}...", verbose)
                time.sleep(RETRY_DELAY)
                continue
            return {
                "status": "timeout",
                "error": f"请求超时（{timeout}秒）",
                "suggestion": "请检查网络连接，或尝试增加超时时间"
            }
        except Exception as e:
            if attempt < MAX_RETRIES:
                print_progress(f"发生错误，重试 {attempt + 1}/{MAX_RETRIES}...", verbose)
                time.sleep(RETRY_DELAY)
                continue
            return {
                "status": "error",
                "error": str(e)
            }
    
    # 所有重试都失败
    return {
        "status": "error",
        "error": "多次尝试后仍失败",
        "suggestion": "请尝试使用浏览器模式：python tool.py <链接> browser"
    }


def validate_url(url: str) -> tuple[bool, str]:
    """
    验证 URL 格式和安全性
    
    Returns:
        (is_valid, error_message)
    """
    # 检查是否为微信公众号链接
    if not re.match(r'https://mp\.weixin\.qq\.com/s/', url):
        return False, "无效的微信公众号文章链接（应为 https://mp.weixin.qq.com/s/... 格式）"
    
    # 安全检查：防止 SSRF 攻击
    parsed = re.match(r'https://([^/]+)', url)
    if parsed:
        domain = parsed.group(1)
        if domain != 'mp.weixin.qq.com':
            return False, f"只允许访问 mp.weixin.qq.com，当前域名：{domain}"
    
    return True, ""


def read_article(url: str, method: str = "auto", timeout: int = DEFAULT_TIMEOUT, verbose: bool = True) -> dict:
    """
    读取微信公众号文章（优化版）
    
    Args:
        url: 文章链接
        method: 读取方法 ("auto" | "fetch" | "browser")
        timeout: 超时时间（秒）
        verbose: 是否输出进度信息
    
    Returns:
        dict: 包含文章内容的字典
    """
    # 验证 URL 格式和安全性
    is_valid, error_msg = validate_url(url)
    if not is_valid:
        return {
            "status": "error",
            "error": error_msg
        }
    
    print_progress(f"开始读取文章：{url[:50]}...", verbose)
    print_progress(f"使用模式：{method}", verbose)
    
    if method == "auto":
        # 先尝试直接抓取（快速，适用于 80% 的公开文章）
        result = read_with_fetch(url, timeout=timeout, verbose=verbose)
        
        if result["status"] == "ok":
            return result
        
        # 如果需要验证或提取失败，尝试浏览器方式
        if result["status"] in ["captcha_required", "extract_failed", "network_error", "timeout"]:
            print_progress("直接抓取失败，切换到浏览器模式...", verbose)
            return read_with_browser(url, timeout=timeout, verbose=verbose)
        
        # 其他错误直接返回
        return result
    
    elif method == "fetch":
        return read_with_fetch(url, timeout=timeout, verbose=verbose)
    
    elif method == "browser":
        return read_with_browser(url, timeout=timeout, verbose=verbose)
    
    else:
        return {
            "status": "error",
            "error": f"未知的方法：{method}",
            "suggestion": "可用方法：auto（默认）、fetch（直接抓取）、browser（浏览器）"
        }


def format_output(result: dict, include_stats: bool = True) -> str:
    """
    格式化输出结果（优化版）
    
    改进：
    - 显示统计信息（图片数、链接数、字数）
    - 更好的错误提示
    - 保留建议信息
    """
    if result["status"] != "ok":
        error_msg = result.get("error", "未知错误")
        suggestion = result.get("suggestion", "")
        
        output = f"❌ 读取失败：{error_msg}"
        if suggestion:
            output += f"\n\n💡 建议：{suggestion}"
        
        # 如果有部分成功（如提取到了标题）
        if result.get("title"):
            output += f"\n\n📰 文章标题：{result['title']}"
        
        return output
    
    output = []
    
    # 标题
    if result["title"]:
        output.append(f"# {result['title']}")
        output.append("")
    
    # 元信息
    meta_lines = []
    if result.get("author"):
        meta_lines.append(f"作者：{result['author']}")
    if result.get("account"):
        meta_lines.append(f"公众号：{result['account']}")
    if result.get("publish_time"):
        meta_lines.append(f"发布时间：{result['publish_time']}")
    
    if meta_lines:
        output.append(" | ".join(meta_lines))
        output.append("")
        output.append("---")
        output.append("")
    
    # 正文
    if result["content"]:
        output.append(result["content"])
        output.append("")
    
    # 统计信息
    if include_stats:
        stats = []
        word_count = len(result["content"]) if result.get("content") else 0
        if word_count > 0:
            stats.append(f"{word_count} 字")
        if result.get("images"):
            stats.append(f"{len(result['images'])} 张图片")
        if result.get("links"):
            stats.append(f"{len(result['links'])} 个链接")
        
        if stats:
            output.append("---")
            output.append(f"📊 统计：{', '.join(stats)}")
            output.append("")
    
    # 原文链接
    if result["url"]:
        output.append(f"📎 原文链接：{result['url']}")
    
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
