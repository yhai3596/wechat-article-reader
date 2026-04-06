# GitHub Release Notes Template

## Copy this for GitHub Release

---

## 🎉 wechat-article-reader v2.0.0

**Release Date:** 2026-04-06

A major optimization release with significant improvements to user experience, error handling, and content extraction.

---

## ✨ What's New

### 🔄 Progress Indicators
Real-time display of reading progress - know exactly what's happening at each step!
```
🔄 Starting to read article...
🔄 Using mode: auto
🔄 Trying direct fetch...
🔄 Direct fetch successful ✓
```

### 🎯 Error Classification
Clear distinction between different error types with actionable suggestions:
- `captcha_required` - Manual verification needed
- `network_error` - Network connection issues
- `extract_failed` - Content extraction failure
- `not_found` - Article deleted or doesn't exist
- `timeout` - Request timeout

### 🖼️ Content Format Preservation
- Images preserved as Markdown: `![alt](url)`
- Links preserved: `[text](url)`
- Bold and italic text formatting
- Proper paragraph separation

### 📊 Statistics Display
Automatic display of:
- Word count
- Number of images
- Number of links

### 🔄 Auto-Retry Mechanism
Automatically retries up to 2 times on network fluctuations for better reliability.

### ⚡ Smart Fallback
Auto mode intelligently switches from direct fetch to browser mode when needed.

### 🛡️ Security Enhancements
URL validation to prevent SSRF attacks - only allows mp.weixin.qq.com domain.

### 🌐 Bilingual Documentation
- README.md (中文)
- README_en.md (English)

---

## 📦 Installation

### Via ClawHub (Recommended)
```bash
npx clawhub@latest install wechat-article-reader
```

### From GitHub
```bash
git clone https://github.com/yhai3596/wechat-article-reader.git \
  ~/.openclaw/skills/wechat-article-reader
cd ~/.openclaw/skills/wechat-article-reader
pip install playwright
playwright install chromium
```

---

## 🚀 Usage

### Basic Usage
```bash
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx"
```

### Advanced Options
```bash
# Browser mode (for verified articles)
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" browser

# JSON output (for programmatic use)
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" --json

# Quiet mode (no progress display)
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" --quiet

# View help
python3 tool.py --help
```

---

## 📝 Example Output

### Success
```markdown
# Article Title

作者：Author | 公众号：Account | 发布时间：2026-04-05 22:29

---

Article content...

![Image](https://...)

[Link](https://...)

---
📊 统计：4431 字，1 张图片

📎 原文链接：https://mp.weixin.qq.com/s/xxxxx
```

### Verification Required
```
❌ 读取失败：需要用户手动验证

💡 建议：请在打开的浏览器窗口中完成验证（滑块或扫码），
        验证后关闭窗口并重新运行。验证后会话将保持约 24 小时。
```

---

## 🐛 Bug Fixes

- Fixed image extraction not preserving URLs
- Fixed link extraction losing href attributes
- Fixed HTML entity decoding issues
- Fixed browser process singleton lock errors
- Fixed timeout handling in direct fetch mode

---

## 📚 Documentation

- **README (中文)**: https://github.com/yhai3596/wechat-article-reader/blob/main/README.md
- **README (English)**: https://github.com/yhai3596/wechat-article-reader/blob/main/README_en.md
- **Changelog**: https://github.com/yhai3596/wechat-article-reader/blob/main/CHANGELOG.md
- **Skill Doc**: https://github.com/yhai3596/wechat-article-reader/blob/main/SKILL.md

---

## 🔗 Links

- **Repository**: https://github.com/yhai3596/wechat-article-reader
- **Issues**: https://github.com/yhai3596/wechat-article-reader/issues
- **Discussions**: https://github.com/yhai3596/wechat-article-reader/discussions
- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.ai

---

## 👤 Author

**小爪 (Claw)** 🦎

Based on OpenClaw framework.

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🙏 Acknowledgments

- [OpenClaw](https://openclaw.ai) - AI Assistant Framework
- [ClawHub](https://clawhub.ai) - Skill Marketplace
- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) - Inspiration

---

**Full Changelog**: https://github.com/yhai3596/wechat-article-reader/compare/v1.0.0...v2.0.0
