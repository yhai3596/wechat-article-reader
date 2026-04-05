---
name: wechat-article-reader
description: "读取微信公众号文章全文。支持直接抓取和浏览器自动化模式，自动处理微信反爬验证。"
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
            "browser_user_data_dir": "~/.openclaw/browser/openclaw/user-data"
          }
      }
  }
---

# 微信公众号文章读取技能

读取微信公众号文章全文内容，支持直接抓取和浏览器自动化两种模式。

## 何时使用

✅ **使用此技能：**

- "读取这篇公众号文章：[链接]"
- "帮我获取微信文章的内容"
- "下载公众号文章"
- 需要分析、总结、翻译公众号文章

❌ **不使用此技能：**

- 非微信公众号链接（使用 web_fetch）
- 需要下载文章中的视频/音频（仅支持文本）
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

AI 会自动调用此技能。

### 方式 2：命令行调用

```bash
python3 ~/.openclaw/skills/wechat-article-reader/tool.py \
  "https://mp.weixin.qq.com/s/xxxxx"
```

### 方式 3：Python API

```python
from wechat_reader import read_article, format_output

result = read_article("https://mp.weixin.qq.com/s/xxxxx")
if result["status"] == "ok":
    print(format_output(result))
```

## 工作原理

### 模式 1：直接抓取（默认）

- 使用 curl 模拟浏览器请求
- 适用于约 80% 的公开文章
- 无需验证，2-5 秒响应

### 模式 2：浏览器自动化

- 使用 Playwright 控制 Chrome
- 适用于需要验证的文章
- 需要用户先手动完成验证

### 验证流程

部分文章会遇到"环境异常，需要验证"：

1. AI 打开浏览器访问文章链接
2. 页面显示验证提示
3. **用户在浏览器中完成验证**（滑块/扫码）
4. 验证后会话保持数小时至数天
5. 重新读取即可成功

## 输出格式

```markdown
# 文章标题

**作者**: 作者名
**公众号**: 公众号名称
**发布时间**: 2024-01-01 12:00

---

正文内容...

---

**原文链接**: https://mp.weixin.qq.com/s/xxxxx
```

## 配置

在 `TOOLS.md` 中添加：

```markdown
## 微信公众号文章读取

- 浏览器用户数据目录：`~/.openclaw/browser/openclaw/user-data`
- 验证后会话保持时间：约 24 小时
```

## 故障排查

### 问题：一直提示"需要验证"

**解决**：
1. 用浏览器打开文章链接
2. 完成验证
3. 保持浏览器窗口打开
4. 重新运行技能

### 问题：Playwright 未安装

**解决**：
```bash
pip install playwright
playwright install chromium
```

### 问题：Chrome 未找到

**解决**：
```bash
# Ubuntu/Debian
sudo apt install google-chrome-stable

# macOS
brew install --cask google-chrome
```

## 限制说明

- ❌ 付费文章可能无法访问
- ❌ 已删除的文章无法读取
- ❌ 视频、音频仅保留链接
- ❌ 图片以链接形式保留，不下载
- ⚠️ 高频访问可能触发风控

## 替代方案

如果此技能无法满足需求：

1. **wechat-article-exporter** (在线服务)
   - 网址：https://down.mptext.top
   - 无需安装，直接使用

2. **wechat-reader** (专业工具)
   - GitHub: https://github.com/xiguawang/wechat-reader
   - 提供更稳定的读取能力

## 开发信息

- **作者**: 小爪 (Claw) 🦎
- **版本**: v1.0
- **许可证**: MIT
- **GitHub**: https://github.com/yhai3596/wechat-article-reader

## 相关文件

- `SKILL.md` - 此文件，技能说明
- `README.md` - 详细使用文档
- `wechat_reader.py` - 核心读取模块
- `tool.py` - 命令行工具入口
