# WeChat Article Reader Skill

📰 OpenClaw Skill for reading full text of WeChat Official Account articles

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/yhai3596/wechat-article-reader)
[![GitHub stars](https://img.shields.io/github/stars/yhai3596/wechat-article-reader?style=social)](https://github.com/yhai3596/wechat-article-reader)

**[🌐 English Version](README_en.md)** | **[📖 中文文档](README.md)**

---

## ✨ Features

- 🚀 **One-Click Reading**: Send a link to get the full text
- 🔍 **Smart Extraction**: Automatically extracts title, author, publish time, and content
- 🛡️ **Anti-Scraping Handling**: Supports browser verification mode to bypass WeChat anti-scraping
- 📦 **Easy Installation**: Supports one-click installation via ClawHub
- 🎯 **High Success Rate**: ~80% of articles can be fetched directly
- 🆕 **v2.0 Optimizations**: Progress indicators, error classification, image format preservation, auto-retry

### 🆕 New Features in v2.0

| Feature | Description |
|---------|-------------|
| 🔄 **Progress Indicators** | Real-time display of reading progress (browser launch, page load, content extraction, etc.) |
| 🎯 **Error Classification** | Clear distinction: network errors, verification required, content extraction failure, article not found, etc. |
| 🖼️ **Image Preservation** | Images preserved in Markdown format `![alt](url)` |
| 🔗 **Link Preservation** | Links in text preserved as `[text](url)` |
| 📊 **Statistics** | Displays word count, number of images, number of links |
| 🔄 **Auto-Retry** | Automatically retries up to 2 times on network fluctuations |
| ⚡ **Smart Fallback** | Automatically switches to browser mode when direct fetch fails |
| 🛡️ **URL Validation** | Prevents SSRF attacks, only allows mp.weixin.qq.com |

---

## 🚀 Quick Start

### Installation

#### Method 1: Via ClawHub (Recommended)

```bash
npx clawhub@latest install wechat-article-reader
```

#### Method 2: From GitHub

```bash
git clone https://github.com/yhai3596/wechat-article-reader.git \
  ~/.openclaw/skills/wechat-article-reader
cd ~/.openclaw/skills/wechat-article-reader
pip install playwright
playwright install chromium
```

#### Method 3: Manual Copy

Copy the entire `wechat-article-reader` folder to `~/.openclaw/skills/` directory

### Usage

#### In OpenClaw Chat

Send the WeChat article link directly:

```
Read this WeChat article:
https://mp.weixin.qq.com/s/xxxxx
```

AI will automatically call the skill and display progress indicators.

#### Command Line

```bash
# Basic usage (auto mode)
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx"

# Specify mode
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" browser
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" fetch

# Output JSON format
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" --json

# Quiet mode (no progress display)
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx" --quiet

# View help
python3 tool.py --help
```

#### Python API

```python
from wechat_reader import read_article, format_output

# Basic usage
result = read_article("https://mp.weixin.qq.com/s/xxxxx")
if result["status"] == "ok":
    print(format_output(result))

# With parameters
result = read_article(
    "https://mp.weixin.qq.com/s/xxxxx",
    method="browser",  # auto | fetch | browser
    timeout=60,         # timeout in seconds
    verbose=True        # show progress
)
```

---

## 🔧 How It Works

### Mode 1: Direct Fetch (Default)

- Uses curl to simulate browser requests
- Works for ~80% of public articles
- No verification required, 2-5 seconds response
- Auto-retries up to 2 times on network fluctuations

### Mode 2: Browser Automation

- Uses Playwright to control Chrome/Chromium
- For articles requiring verification
- Real-time progress indicators
- Session persists for ~24 hours

### Smart Fallback Strategy

```
Auto mode workflow:
1. Try direct fetch (fast)
   ├─ Success → Return result
   └─ Failure → Check failure reason
       ├─ Verification required → Switch to browser mode
       ├─ Network error → Retry up to 2 times
       └─ Extraction failed → Switch to browser mode
2. Browser mode
   ├─ Launch browser
   ├─ Load page
   ├─ Check verification
   └─ Extract content
```

---

## 🎯 Examples

### Input

```
Read this WeChat article:
https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw
```

### Output (Success)

```
🔄 Starting to read article: https://mp.weixin.qq.com/s/...
🔄 Using mode: auto
🔄 Trying direct fetch...
🔄 Direct fetch successful ✓ (Title: ...)

# Article Title

Author: Author Name | Account: Account Name | Publish Time: 2026-04-05 22:29

---

Article content...

![Image Description](https://...)

Link in text [Click Here](https://...)

---
📊 Statistics: 1523 words, 3 images, 2 links

📎 Original Link: https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw
```

### Output (Verification Required)

```
🔄 Starting to read article: https://mp.weixin.qq.com/s/...
🔄 Using mode: auto
🔄 Trying direct fetch...
⚠️  Verification required
🔄 Direct fetch failed, switching to browser mode...
🔄 Launching browser...
🔄 Browser launched ✓
🔄 Accessing article link...
⚠️  Verification required

❌ Read failed: Manual verification required

💡 Suggestion: Please complete verification (slider or QR code) in the opened browser window, close the window and re-run. Session will persist for ~24 hours after verification.

📝 Note: WeChat detected abnormal access and requires security verification. This is normal and can be used multiple times after one verification.
```

---

## ⚠️ Notes

### Verification Issues

Some articles may encounter "Environment abnormal, verification required":

1. 🌐 Browser automatically opens to access the article link
2. ⚠️ Page displays verification prompt (slider or QR code)
3. 👤 **User completes verification in browser**
4. ✅ Session persists for ~24 hours after verification
5. 🔄 Re-run to successfully read

### Limitations

- ❌ Paid articles may not be accessible
- ❌ Deleted articles cannot be read
- ❌ Videos/audio only preserve links (not downloaded)
- ✅ Images preserved in Markdown format `![alt](url)` (not downloaded)
- ⚠️ High-frequency access may trigger risk control (recommend 5+ seconds interval)

---

## 🛠️ Troubleshooting

### Issue 1: Always prompts "Verification Required"

**Symptoms**:
```
❌ Read failed: Manual verification required
💡 Suggestion: Please access the link in browser to complete verification, then re-run
```

**Solution**:
1. 🌐 Open the article link in a browser
2. ✅ Complete verification (slider or QR code)
3. 🔄 Re-run the skill
4. ⏰ Session persists for ~24 hours after verification, can read directly during this period

---

### Issue 2: Playwright Not Installed

**Symptoms**:
```
❌ Read failed: Playwright not installed
```

**Solution**:
```bash
pip install playwright
playwright install chromium
```

---

### Issue 3: Chrome/Chromium Not Found

**Symptoms**:
```
❌ Read failed: Browser error: ...
```

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install google-chrome-stable

# macOS
brew install --cask google-chrome

# Or use Playwright's built-in Chromium
playwright install chromium
```

---

### Issue 4: Article Not Found or Deleted

**Symptoms**:
```
❌ Read failed: Article does not exist or has been deleted
```

**Solution**:
- Verify the link is correct
- Article may have been deleted by the publisher
- Cannot be recovered, contact the author for access

---

### Issue 5: Network Connection Failed

**Symptoms**:
```
❌ Read failed: Network connection failed
```

**Solution**:
- Check network connection
- WeChat server may be temporarily unavailable
- Retry later

---

### Issue 6: Content Extraction Failed

**Symptoms**:
```
❌ Read failed: Unable to extract article content
💡 Suggestion: Article may use special formatting, try browser mode
```

**Solution**:
```bash
# Force browser mode
python3 tool.py "<link>" browser
```

---

## 📦 Project Structure

```
wechat-article-reader/
├── SKILL.md           # Skill description (OpenClaw standard format)
├── README.md          # Chinese documentation
├── README_en.md       # English documentation
├── INSTALL.md         # Installation guide
├── wechat_reader.py   # Core reading module (optimized)
├── tool.py            # Command-line tool entry (optimized)
├── package.json       # Skill metadata
└── LICENSE            # MIT License
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

- Bug Reports: https://github.com/yhai3596/wechat-article-reader/issues
- Feature Requests: https://github.com/yhai3596/wechat-article-reader/discussions

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/yhai3596/wechat-article-reader.git
cd wechat-article-reader

# Install dependencies
pip install playwright
playwright install chromium

# Run tests
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx"
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👤 Author

**小爪 (Claw)** 🦎

Developed based on OpenClaw framework

- GitHub: [@yhai3596](https://github.com/yhai3596)
- OpenClaw: https://openclaw.ai

---

## 🙏 Acknowledgments

- [OpenClaw](https://openclaw.ai) - AI Assistant Framework
- [ClawHub](https://clawhub.ai) - Skill Marketplace
- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) - Inspiration

---

## 📮 Contact

For questions or suggestions, feel free to contact via:

- GitHub Issues: https://github.com/yhai3596/wechat-article-reader/issues
- Email: yhai3596@example.com

---

**Found it useful? Give it a ⭐ Star!**
