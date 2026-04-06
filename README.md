# 微信公众号文章读取技能

📰 读取微信公众号文章全文的 OpenClaw Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/yhai3596/wechat-article-reader)
[![GitHub stars](https://img.shields.io/github/stars/yhai3596/wechat-article-reader?style=social)](https://github.com/yhai3596/wechat-article-reader)

**[🌐 English Version](README_en.md)** | **[📖 中文文档](README.md)**

---

## ✨ 特性

- 🚀 **一键读取**：发送链接即可获取全文
- 🔍 **智能提取**：自动提取标题、作者、发布时间、正文
- 🛡️ **反爬处理**：支持浏览器验证模式，绕过微信反爬
- 📦 **易于安装**：支持 ClawHub 一键安装
- 🎯 **高成功率**：约 80% 文章可直接抓取
- 🆕 **v2.0 优化**：进度提示、错误分类、保留图片格式、自动重试

### 🆕 v2.0 新增功能

| 功能 | 说明 |
|------|------|
| 🔄 **进度提示** | 实时显示读取进度（启动浏览器、加载页面、提取内容等） |
| 🎯 **错误分类** | 清晰区分：网络错误、验证需求、内容提取失败、文章不存在等 |
| 🖼️ **保留图片** | 图片以 Markdown 格式 `![alt](url)` 保留 |
| 🔗 **保留链接** | 文中链接完整保留为 `[text](url)` |
| 📊 **统计信息** | 显示字数、图片数、链接数 |
| 🔄 **自动重试** | 网络波动时自动重试 2 次 |
| ⚡ **智能降级** | 直接抓取失败自动切换浏览器模式 |
| 🛡️ **URL 验证** | 防止 SSRF 攻击，只允许 mp.weixin.qq.com |

---

## 🚀 快速开始

### 安装

#### 方法 1：通过 ClawHub（推荐）

```bash
npx clawhub@latest install wechat-article-reader
```

#### 方法 2：从 GitHub 安装

```bash
git clone https://github.com/yhai3596/wechat-article-reader.git \
  ~/.openclaw/skills/wechat-article-reader
cd ~/.openclaw/skills/wechat-article-reader
pip install playwright
playwright install chromium
```

#### 方法 3：手动复制

复制整个 `wechat-article-reader` 文件夹到 `~/.openclaw/skills/` 目录

### 使用

#### 在 OpenClaw 对话中

直接发送公众号文章链接：

```
读取这篇公众号文章：
https://mp.weixin.qq.com/s/xxxxx
```

AI 会自动调用技能，并显示进度提示。

#### 命令行调用

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

# 查看帮助
python3 tool.py --help
```

#### Python API

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

---

## 🔧 工作原理

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

### 智能降级策略

```
auto 模式工作流程：
1. 尝试直接抓取（快速）
   ├─ 成功 → 返回结果
   └─ 失败 → 检查失败原因
       ├─ 需要验证 → 切换到浏览器模式
       ├─ 网络错误 → 重试 2 次
       └─ 提取失败 → 切换到浏览器模式
2. 浏览器模式
   ├─ 打开浏览器
   ├─ 加载页面
   ├─ 检查验证
   └─ 提取内容
```

---

## 🎯 示例

### 输入

```
读取这篇公众号文章：
https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw
```

### 输出（成功）

```
🔄 开始读取文章：https://mp.weixin.qq.com/s/...
🔄 使用模式：auto
🔄 正在尝试直接抓取...
🔄 直接抓取成功 ✓ (标题：美伊战争的经济账 / AI Tokens...)

# 美伊战争的经济账 / AI Tokens 的经济账

作者：某作者 | 公众号：某公众号 | 发布时间：2026-04-05 22:29

---

正文内容...

![图片描述](https://...)

文中链接 [点击这里](https://...)

---
📊 统计：1523 字，3 张图片，2 个链接

📎 原文链接：https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw
```

### 输出（需要验证）

```
🔄 开始读取文章：https://mp.weixin.qq.com/s/...
🔄 使用模式：auto
🔄 正在尝试直接抓取...
⚠️  需要验证
🔄 直接抓取失败，切换到浏览器模式...
🔄 正在启动浏览器...
🔄 浏览器已启动 ✓
🔄 正在访问文章链接...
⚠️  需要验证

❌ 读取失败：需要用户手动验证

💡 建议：请在打开的浏览器窗口中完成验证（滑块或扫码），验证后关闭窗口并重新运行。验证后会话将保持约 24 小时。

📝 说明：微信检测到异常访问，需要完成安全验证。这是正常现象，验证一次后可多次使用。
```

---

## ⚠️ 注意事项

### 验证问题

部分文章会遇到"环境异常，需要验证"：

1. 🌐 自动打开浏览器访问文章链接
2. ⚠️ 页面显示验证提示（滑块或扫码）
3. 👤 **用户在浏览器中完成验证**
4. ✅ 验证后会话保持约 24 小时
5. 🔄 重新运行即可成功读取

### 限制说明

- ❌ 付费文章可能无法访问
- ❌ 已删除的文章无法读取
- ❌ 视频、音频仅保留链接（不下载）
- ✅ 图片以 Markdown 格式保留 `![alt](url)`（不下载）
- ⚠️ 高频访问可能触发风控（建议间隔 5 秒以上）

---

## 🛠️ 故障排查

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

---

## 📦 项目结构

```
wechat-article-reader/
├── SKILL.md           # 技能说明（OpenClaw 标准格式）
├── README.md          # 中文使用文档
├── README_en.md       # English documentation
├── INSTALL.md         # 安装指南
├── wechat_reader.py   # 核心读取模块（优化版）
├── tool.py            # 命令行工具入口（优化版）
├── package.json       # 技能元数据
└── LICENSE            # MIT 许可证
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- Bug 报告：https://github.com/yhai3596/wechat-article-reader/issues
- 功能建议：https://github.com/yhai3596/wechat-article-reader/discussions

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/yhai3596/wechat-article-reader.git
cd wechat-article-reader

# 安装依赖
pip install playwright
playwright install chromium

# 运行测试
python3 tool.py "https://mp.weixin.qq.com/s/xxxxx"
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👤 作者

**小爪 (Claw)** 🦎

基于 OpenClaw 框架开发

- GitHub: [@yhai3596](https://github.com/yhai3596)
- OpenClaw: https://openclaw.ai

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - AI 助手框架
- [ClawHub](https://clawhub.ai) - 技能市场
- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) - 灵感来源

---

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: https://github.com/yhai3596/wechat-article-reader/issues
- 邮箱：yhai3596@example.com

---

**觉得有用？给个 ⭐ Star 支持一下！**
