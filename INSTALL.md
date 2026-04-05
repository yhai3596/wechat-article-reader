# 安装指南

## 快速安装

### 方法 1：通过 ClawHub（推荐，发布后）

```bash
npx clawhub@latest install wechat-article-reader
```

### 方法 2：从 GitHub 安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/yhai3596/wechat-article-reader.git \
  ~/.openclaw/skills/wechat-article-reader

# 进入目录
cd ~/.openclaw/skills/wechat-article-reader

# 安装 Python 依赖
pip install playwright

# 安装浏览器
playwright install chromium
```

### 方法 3：手动复制

1. 下载或复制整个 `wechat-article-reader` 文件夹
2. 放到 `~/.openclaw/skills/` 目录下
3. 运行安装命令

## 系统要求

### 必需

- **Python**: 3.8+
- **curl**: 已预装在大多数系统
- **Chrome/Chromium**: 浏览器（playwright 会自动安装）

### 可选

- **Node.js**: 用于使用 ClawHub 安装

## 详细安装步骤

### 步骤 1：检查 Python

```bash
python3 --version
# 应该显示 Python 3.8 或更高版本
```

如果未安装 Python：

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS
brew install python

# Windows
# 从 https://python.org 下载安装
```

### 步骤 2：安装 Playwright

```bash
pip install playwright
```

如果遇到权限问题：

```bash
# 使用 --user 参数
pip install --user playwright

# 或使用 sudo（不推荐）
sudo pip install playwright
```

### 步骤 3：安装浏览器

```bash
playwright install chromium
```

这会下载 Chromium 浏览器（约 150MB）。

### 步骤 4：验证安装

```bash
# 测试技能
python3 tool.py "https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw"
```

如果看到文章内容，说明安装成功！

## 故障排查

### 问题：pip 未找到

**解决**：
```bash
# 检查 pip 是否在 PATH 中
which pip3

# 如果不在，尝试使用 python3 -m pip
python3 -m pip install playwright
```

### 问题：权限错误

**解决**：
```bash
# 使用 --user 参数
pip install --user playwright

# 或创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install playwright
```

### 问题：Chrome 未找到

**解决**：
```bash
# Ubuntu/Debian
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt update
sudo apt install google-chrome-stable

# macOS
brew install --cask google-chrome

# 或使用 playwright 自带的 Chromium
playwright install chromium
```

### 问题：playwright install chromium 失败

**解决**：
```bash
# 检查网络连接
ping playwright.dev

# 使用国内镜像（如果在中国）
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

## 验证安装

运行测试：

```bash
python3 tool.py "https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw"
```

期望输出：
- 文章标题
- 作者信息
- 正文内容
- 原文链接

## 在 OpenClaw 中使用

安装完成后，在对话中直接发送：

```
读取这篇公众号文章：
https://mp.weixin.qq.com/s/xxxxx
```

AI 会自动调用此技能。

## 下一步

安装成功后，查看：
- [使用文档](README.md) - 详细使用方法
- [技能说明](SKILL.md) - 技能规范和配置

## 帮助

如有问题，请查看：
- GitHub Issues: https://github.com/yhai3596/wechat-article-reader/issues
- 文档：https://github.com/yhai3596/wechat-article-reader/blob/main/README.md
