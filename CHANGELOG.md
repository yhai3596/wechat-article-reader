# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-04-06

### 🎉 Major Optimizations

This is a major release with significant improvements to user experience, error handling, and content extraction.

### ✨ Added

- **Progress Indicators** - Real-time display of reading progress
  - Browser launch status
  - Page loading progress
  - Content extraction status
  - Success/failure indicators with checkmarks (✓) and warnings (⚠️)

- **Error Classification** - Clear distinction between different error types
  - `captcha_required` - Manual verification needed
  - `network_error` - Network connection issues
  - `extract_failed` - Content extraction failure
  - `not_found` - Article deleted or doesn't exist
  - `timeout` - Request timeout
  - `browser_error` - Browser launch/operation errors

- **Actionable Suggestions** - Each error now includes helpful suggestions
  - Step-by-step guidance for verification
  - Installation commands for missing dependencies
  - Alternative solutions for persistent issues

- **Content Format Preservation**
  - Images preserved as Markdown: `![alt](url)`
  - Links preserved as Markdown: `[text](url)`
  - Bold text: `**text**`
  - Italic text: `*text*`
  - Line breaks and paragraphs properly formatted

- **Statistics Display**
  - Word count
  - Number of images
  - Number of links

- **Auto-Retry Mechanism**
  - Automatically retries up to 2 times on network fluctuations
  - Configurable retry count
  - Delay between retries to avoid rate limiting

- **Smart Fallback**
  - Auto mode automatically switches from direct fetch to browser mode on failure
  - Intelligent error handling to determine when to fallback

- **URL Security Validation**
  - Prevents SSRF attacks
  - Only allows mp.weixin.qq.com domain
  - Clear error messages for invalid URLs

- **Command Line Options**
  - `--json` - Output in JSON format for programmatic processing
  - `--quiet` - Silent mode, suppresses progress indicators
  - `--help` - Display usage information

- **Bilingual Documentation**
  - README.md (Chinese)
  - README_en.md (English)

### 🔧 Changed

- **Improved HTML to Markdown Conversion**
  - Complete rewrite of `convert_html_to_markdown()` function
  - Better handling of HTML entities
  - Proper paragraph separation
  - Image and link extraction before tag removal

- **Enhanced Browser Mode**
  - Better error messages with detailed call logs
  - Automatic fallback to Chromium if Chrome is not available
  - Proper browser cleanup on exit
  - User data directory lock handling

- **Optimized Direct Fetch**
  - Better curl parameters for simulating browser requests
  - Improved timeout handling
  - More robust content extraction

- **Documentation Updates**
  - Comprehensive troubleshooting guide with 6 common issues
  - Step-by-step solutions with commands
  - Clear examples of success and failure outputs
  - Project structure documentation

### 🐛 Fixed

- Fixed image extraction not preserving URLs
- Fixed link extraction losing href attributes
- Fixed HTML entity decoding issues
- Fixed browser process singleton lock errors
- Fixed timeout handling in direct fetch mode
- Fixed error message clarity for various failure scenarios

### 📦 Technical Changes

- Added type hints for better code documentation
- Refactored error handling to use structured response objects
- Added configuration constants for timeout and retry settings
- Improved code organization and readability
- Added comprehensive inline documentation

---

## [1.0.0] - 2024-XX-XX

### ✨ Added

- Initial release of wechat-article-reader skill

### Features

- **Two Reading Modes**
  - Direct fetch using curl (fast, ~80% success rate)
  - Browser automation using Playwright (for verified articles)

- **Content Extraction**
  - Title extraction
  - Author extraction
  - Publish time extraction
  - Account name extraction
  - Main content extraction

- **Basic Error Handling**
  - Verification detection
  - Network error handling
  - Timeout handling

- **Installation Support**
  - ClawHub integration
  - Automatic Playwright installation
  - Chromium browser setup

- **Documentation**
  - SKILL.md for OpenClaw integration
  - README.md with usage examples
  - INSTALL.md with detailed installation guide

---

## Version History

| Version | Release Date | Key Changes |
|---------|--------------|-------------|
| 2.0.0 | 2026-04-06 | Major optimizations: progress indicators, error classification, format preservation |
| 1.0.0 | 2024-XX-XX | Initial release |

---

## Upgrade Guide (v1.0 → v2.0)

### Breaking Changes

None! Version 2.0 is fully backward compatible with v1.0.

### New Dependencies

No new external dependencies required. All optimizations use existing libraries.

### Migration Steps

1. **Update the skill**:
   ```bash
   cd ~/.openclaw/skills/wechat-article-reader
   git pull origin main
   ```

2. **Verify installation**:
   ```bash
   python3 tool.py --help
   ```

3. **Test with an article**:
   ```bash
   python3 tool.py "https://mp.weixin.qq.com/s/xxxxx"
   ```

### New Features to Try

- **Progress indicators**: Just run normally, you'll see them automatically
- **JSON output**: Add `--json` flag for programmatic use
- **Quiet mode**: Add `--quiet` flag to suppress progress display
- **Statistics**: Automatically shown at the end of successful reads

---

## Future Roadmap

### Planned for v2.1

- [ ] Caching mechanism for previously read articles
- [ ] Batch reading support for multiple URLs
- [ ] Export to PDF/EPUB format
- [ ] Configurable browser user agent
- [ ] Proxy support for network-restricted environments

### Under Consideration

- [ ] Browser process persistence for faster subsequent reads
- [ ] Automatic captcha solving (where legally permissible)
- [ ] Video/audio transcript extraction
- [ ] Comment section extraction
- [ ] Related articles recommendation

---

## Support

For issues, questions, or suggestions:

- **GitHub Issues**: https://github.com/yhai3596/wechat-article-reader/issues
- **Discussions**: https://github.com/yhai3596/wechat-article-reader/discussions
- **Email**: yhai3596@example.com

---

**Thank you for using wechat-article-reader!** 🦎
