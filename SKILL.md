---
name: wechat-article-reader
description: "读取微信公众号文章全文。支持直接抓取和浏览器自动化模式，自动处理微信反爬验证。优化版：进度提示、错误分类、保留图片格式。"
homepage: https://github.com/yhai3596/wechat-article-reader
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["curl", "python3"], "python_packages": ["playwright"] },
        "install":
          [
            {
              "id": "playwright",
              "kind": "pip",
              "package": "playwright",
              "label": "安装 Playwright (pip)",
              "post_install": ["playwright install chromium"]
            }
          ],
        "config":
          {
            "browser_user_data_dir": "~/.openclaw/browser/openclaw/user-data",
            "timeout_seconds": 30
          }
      }
  }
---

# 微信公众号文章读取技能（优化版）

读取微信公众号文章全文内容，支持直接抓取和浏览器自动化两种模式。

## ✨ 优化特性

- 🚀 **进度提示**：实时显示读取进度
- 🎯 **错误分类**：清晰区分网络错误、验证需求、内容提取失败等
- 🖼️ **保留图片**：图片以 Markdown 格式保留 `![alt](url)`
- 🔗 **保留链接**：文中链接完整保留
- 📊 **统计信息**：显示字数、图片数、链接数
- 🔄 **自动重试**：网络波动时自动重试 2 次
- ⚡ **智能降级**：直接抓取失败自动切换浏览器模式

## 何时使用

✅ **使用此技能：**

- "读取这篇公众号文章：[链接]"
- "帮我获取微信文章的内容"
- "下载公众号文章"
- 需要分析、总结、翻译公众号文章

❌ **不使用此技能：**

- 非微信公众号链接（使用 web_fetch）
- 需要下载文章中的视频/音频（仅保留链接）
- 付费墙文章（可能无法访问）

## 安装

### 自动安装（推荐）

```bash
# 通过 ClawHub（发布后）
npx clawhub@latest install wechat-article-reader
```

### 手动安装

```bash
# 1. 克隆或复制到 skills 目录
git clone https://github.com/your-github-username/wechat-article-reader.git \
  ~/.openclaw/skills/wechat-article-reader

# 2. 安装依赖
cd ~/.openclaw/skills/wechat-article-reader
pip install playwright
playwright install chromium
```

## 使用方法

### 方式 1：对话中直接使用

在对话中发送：

```
读取这篇公众号文章：
https://mp.weixin.qq.com/s/xxxxx
```

AI 会自动调用此技能，并显示进度提示。

### 方式 2：命令行调用

```bash
# 基本用法（自动模式）
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx"

# 指定模式
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" browser
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" fetch

# 输出 JSON 格式
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" --json

# 静默模式（不显示进度）
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" --quiet

# 组合使用
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" browser --json --quiet
```

### 方式 3：Python API

```python
from wechat_reader import read_article, format_output

# 基本用法
result = read_article("https://mp.weixin.qq.com/s/xxxxx")
if result["status"] == "ok":
    print(format_output(result))

# 指定参数
result = read_article(
    "https://mp.weixin.qq.com/s/xxxxx",
    method="browser",  # auto | fetch | browser
    timeout=60,         # 超时时间（秒）
    verbose=True        # 是否显示进度
)
```

## 工作原理

### 模式 1：直接抓取（默认）

- 使用 curl 模拟浏览器请求
- 适用于约 80% 的公开文章
- 无需验证，2-5 秒响应
- 自动重试 2 次（网络波动时）

### 模式 2：浏览器自动化

- 使用 Playwright 控制 Chrome/Chromium
- 适用于需要验证的文章
- 实时显示进度提示
- 会话保持约 24 小时

### 验证流程

部分文章会遇到"环境异常，需要验证"：

1. 🌐 自动打开浏览器访问文章链接
2. ⚠️ 页面显示验证提示（滑块或扫码）
3. 👤 **用户在浏览器中完成验证**
4. ✅ 验证后会话保持约 24 小时
5. 🔄 重新运行即可成功读取

**进度提示示例：**
```
🔄 开始读取文章：https://mp.weixin.qq.com/s/...
🔄 使用模式：auto
🔄 正在尝试直接抓取...
⚠️  需要验证
🔄 直接抓取失败，切换到浏览器模式...
🔄 正在启动浏览器...
🔄 浏览器已启动 ✓
🔄 正在访问文章链接...
🔄 页面已加载 ✓
🔄 正在提取文章内容...
🔄 文章提取成功 ✓ (标题：美伊战争的经济账 / AI Tokens...)
```

## 输出格式

### 成功示例

```markdown
# 美伊战争的经济账 / AI Tokens 的经济账

作者：某作者 | 公众号：某公众号 | 发布时间：2024-01-01 12:00

---

正文内容...

![图片描述](https://...)  # 图片以 Markdown 格式保留

文中链接 [点击这里](https://...)  # 链接完整保留

---
📊 统计：1523 字，3 张图片，2 个链接

📎 原文链接：https://mp.weixin.qq.com/s/xxxxx
```

### 失败示例

```
❌ 读取失败：需要用户手动验证

💡 建议：请先用浏览器访问链接完成验证，然后重新运行

📝 说明：微信检测到异常访问，需要完成安全验证。这是正常现象，验证一次后可多次使用。
```

## 配置

在 `TOOLS.md` 中添加：

```markdown
## 微信公众号文章读取

- 浏览器用户数据目录：`~/.openclaw/browser/openclaw/user-data`
- 验证后会话保持时间：约 24 小时
- 默认超时时间：30 秒
- 最大重试次数：2 次
```

## 故障排查

### 问题 1：一直提示"需要验证"

**现象**：
```
❌ 读取失败：需要用户手动验证
💡 建议：请先用浏览器访问链接完成验证，然后重新运行
```

**解决**：
1. 🌐 用浏览器打开文章链接
2. ✅ 完成验证（滑块或扫码）
3. 🔄 重新运行技能
4. ⏰ 验证后会话保持约 24 小时，期间可直接读取

---

### 问题 2：Playwright 未安装

**现象**：
```
❌ 读取失败：Playwright 未安装
```

**解决**：
```bash
pip install playwright
playwright install chromium
```

---

### 问题 3：Chrome/Chromium 未找到

**现象**：
```
❌ 读取失败：浏览器错误：...
```

**解决**：
```bash
# Ubuntu/Debian
sudo apt install google-chrome-stable

# macOS
brew install --cask google-chrome

# 或使用 Playwright 自带的 Chromium
playwright install chromium
```

---

### 问题 4：文章不存在或已删除

**现象**：
```
❌ 读取失败：文章不存在或已被删除
```

**解决**：
- 确认链接是否正确
- 文章可能已被发布者删除
- 无法恢复，需联系作者获取

---

### 问题 5：网络连接失败

**现象**：
```
❌ 读取失败：网络连接失败
```

**解决**：
- 检查网络连接
- 微信服务器可能暂时不可用
- 稍后重试

---

### 问题 6：内容提取失败

**现象**：
```
❌ 读取失败：无法提取文章内容
💡 建议：文章可能使用了特殊格式，请尝试浏览器模式
```

**解决**：
```bash
# 强制使用浏览器模式
python3 tool.py "<链接>" browser
```

## 限制说明

- ❌ 付费文章可能无法访问
- ❌ 已删除的文章无法读取
- ❌ 视频、音频仅保留链接（不下载）
- ✅ 图片以 Markdown 格式保留 `![alt](url)`（不下载）
- ⚠️ 高频访问可能触发风控（建议间隔 5 秒以上）

## 替代方案

如果此技能无法满足需求：

1. **wechat-article-exporter** (在线服务)
   - 网址：https://down.mptext.top
   - 无需安装，直接使用
   - 适合偶尔使用

2. **wechat-reader** (专业工具)
   - GitHub: https://github.com/xiguawang/wechat-reader
   - 提供更稳定的读取能力
   - 适合批量导出

## 开发信息

- **作者**: 小爪 (Claw) 🦎
- **版本**: v2.0.0 (优化版)
- **许可证**: MIT
- **GitHub**: https://github.com/yhai3596/wechat-article-reader

## 更新日志

完整更新日志请查看 [CHANGELOG.md](CHANGELOG.md)。

### v2.0.0 (2026-04-06) - 重大优化

- ✨ 新增进度提示
- 🎯 错误分类和清晰引导
- 🖼️ 保留图片为 Markdown 格式
- 🔗 保留文中链接
- 📊 显示统计信息（字数、图片数、链接数）
- 🔄 自动重试机制（网络波动时）
- ⚡ 智能降级（直接抓取失败自动切换浏览器）
- 🛡️ URL 安全验证（防止 SSRF）
- 📖 双语文档（中文/英文）

### v1.0.0 - 初始版本

- 基本读取功能
- 支持直接抓取和浏览器两种模式

### v2.0 (优化版)
- ✨ 新增进度提示
- 🎯 错误分类和清晰引导
- 🖼️ 保留图片为 Markdown 格式
- 🔗 保留文中链接
- 📊 显示统计信息（字数、图片数、链接数）
- 🔄 自动重试机制（网络波动时）
- ⚡ 智能降级（直接抓取失败自动切换浏览器）
- 🛡️ URL 安全验证（防止 SSRF）

### v1.0 (初始版)
- 基本读取功能
- 支持直接抓取和浏览器两种模式

## 相关文件

- `SKILL.md` - 此文件，技能说明
- `README.md` - 详细使用文档
- `wechat_reader.py` - 核心读取模块（优化版）
- `tool.py` - 命令行工具入口（优化版）
