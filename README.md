# 微信公众号文章读取技能

📰 读取微信公众号文章全文的 OpenClaw Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)

## ✨ 特性

- 🚀 **一键读取**：发送链接即可获取全文
- 🔍 **智能提取**：自动提取标题、作者、发布时间、正文
- 🛡️ **反爬处理**：支持浏览器验证模式，绕过微信反爬
- 📦 **易于安装**：支持 ClawHub 一键安装
- 🎯 **高成功率**：约 80% 文章可直接抓取

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

#### 命令行调用

```bash
python3 ~/.openclaw/skills/wechat-article-reader/tool.py \
  "https://mp.weixin.qq.com/s/xxxxx"
```

#### Python API

```python
from wechat_reader import read_article, format_output

result = read_article("https://mp.weixin.qq.com/s/xxxxx")
if result["status"] == "ok":
    print(format_output(result))
```

## 📖 文档

- [📦 安装指南](INSTALL.md) - 详细安装步骤
- [📚 技能说明](SKILL.md) - 技能规范和使用指南
- [📋 发布规划](PUBLISH.md) - 发布和版本管理
- [📝 交付文档](DELIVERY.md) - 功能说明和测试结果

## 🔧 工作原理

### 模式 1：直接抓取（默认）

- 使用 curl 模拟浏览器请求
- 适用于约 80% 的公开文章
- 无需验证，2-5 秒响应

### 模式 2：浏览器自动化

- 使用 Playwright 控制 Chrome
- 适用于需要验证的文章
- 需要用户先手动完成验证

## ⚠️ 注意事项

### 验证问题

部分文章会遇到"环境异常，需要验证"：

1. 用浏览器打开文章链接
2. 完成验证（滑块/扫码）
3. 验证后会话保持数小时至数天
4. 重新读取即可成功

### 限制说明

- ❌ 付费文章可能无法访问
- ❌ 已删除的文章无法读取
- ❌ 视频、音频仅保留链接
- ❌ 图片以链接形式保留，不下载

## 🎯 示例

### 输入

```
读取这篇公众号文章：
https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw
```

### 输出

```markdown
# 美伊战争的经济账 / AI Tokens 的经济账

**发布时间**: 2026-04-05 22:29

---

正文内容...

---

**原文链接**: https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw
```

## 🛠️ 开发

### 项目结构

```
wechat-article-reader/
├── SKILL.md           # 技能说明（OpenClaw 标准格式）
├── README.md          # 本文件
├── INSTALL.md         # 安装指南
├── wechat_reader.py   # 核心读取模块
├── tool.py            # 命令行工具入口
├── package.json       # 技能元数据
└── LICENSE            # MIT 许可证
```

### 本地测试

```bash
cd ~/.openclaw/skills/wechat-article-reader
python3 tool.py "https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw"
```

### 依赖

- Python 3.8+
- curl
- Playwright
- Chromium（Playwright 自动安装）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- Bug 报告：https://github.com/yhai3596/wechat-article-reader/issues
- 功能建议：https://github.com/yhai3596/wechat-article-reader/discussions

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

**小爪 (Claw)** 🦎

基于 OpenClaw 框架开发

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - AI 助手框架
- [ClawHub](https://clawhub.ai) - 技能市场
- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) - 灵感来源

---

**觉得有用？给个 ⭐ Star 支持一下！**
