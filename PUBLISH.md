# 📋 发布规划 - wechat-article-reader Skill

## 任务目标

将微信公众号文章读取功能封装成**可安装、可分享的 OpenClaw Skill**，让其他"小龙虾"能够轻松使用。

---

## ✅ 已完成工作

### 1. 技能重构

- ✅ 标准化 `SKILL.md` 格式（符合 OpenClaw 规范）
- ✅ 添加 `metadata` 配置（emoji、依赖、安装步骤）
- ✅ 创建 `package.json`（技能元数据）
- ✅ 创建 `.gitignore`（排除不必要文件）

### 2. 文档完善

- ✅ `SKILL.md` - 技能说明和使用指南
- ✅ `README.md` - 详细使用文档
- ✅ `INSTALL.md` - 安装指南
- ✅ `DELIVERY.md` - 交付文档
- ✅ `PUBLISH.md` - 本规划文档

### 3. 工具脚本

- ✅ `wechat_reader.py` - 核心读取模块
- ✅ `tool.py` - 命令行工具入口
- ✅ `publish.sh` - 发布脚本

### 4. 测试验证

- ✅ 测试链接成功获取
- ✅ 直接抓取模式工作正常
- ✅ 输出格式符合预期

---

## 📦 发布方案

### 方案 A：GitHub + ClawHub（推荐）⭐

**优点**：
- ✅ 版本管理清晰
- ✅ 易于分享和传播
- ✅ 支持一键安装
- ✅ 社区可见

**步骤**：

1. **创建 GitHub 仓库**
   ```bash
   # 在 GitHub 上创建新仓库
   # 名称：wechat-article-reader
   # 可见性：Public
   ```

2. **推送代码**
   ```bash
   cd /home/13928293596_wy/openclaw/workspace/skills/wechat-article-reader
   
   # 初始化 Git（如果还没有）
   git init
   git add -A
   git commit -m "initial release: wechat-article-reader skill"
   
   # 添加远程仓库（替换为你的 GitHub 用户名）
   git remote add origin https://github.com/YOUR_USERNAME/wechat-article-reader.git
   
   # 推送
   git push -u origin main
   ```

3. **发布到 ClawHub**
   ```bash
   # 使用发布脚本
   bash publish.sh
   
   # 或手动发布
   npx clawhub@latest publish
   ```

4. **验证安装**
   ```bash
   # 测试安装（从 GitHub）
   git clone https://github.com/YOUR_USERNAME/wechat-article-reader.git \
     ~/.openclaw/skills/wechat-article-reader
   
   # 测试功能
   python3 ~/.openclaw/skills/wechat-article-reader/tool.py \
     "https://mp.weixin.qq.com/s/4gmDz_VsBZ1qIaEINQGxcw"
   ```

---

### 方案 B：仅 GitHub

**适用场景**：不想发布到 ClawHub，仅通过 GitHub 分享

**步骤**：

1. 创建 GitHub 仓库（同上）
2. 推送代码（同上）
3. 在 README 中添加安装说明

**安装命令**（给其他用户）：
```bash
git clone https://github.com/YOUR_USERNAME/wechat-article-reader.git \
  ~/.openclaw/skills/wechat-article-reader
cd ~/.openclaw/skills/wechat-article-reader
pip install playwright
playwright install chromium
```

---

### 方案 C：ClawHub 独占

**适用场景**：不想公开源代码，仅通过 ClawHub 分发

**步骤**：

1. 打包技能目录
2. 通过 ClawHub CLI 发布
3. 设置访问权限

---

## 🎯 推荐执行路径

### 阶段 1：准备（已完成 80%）

- [x] 技能代码开发
- [x] 测试验证
- [x] 文档编写
- [ ] 更新 GitHub 用户名（在 package.json 等文件中）
- [ ] 添加 LICENSE 文件

### 阶段 2：GitHub 发布（立即可做）

- [ ] 在 GitHub 创建仓库
- [ ] 推送代码
- [ ] 设置仓库描述和标签
- [ ] 添加 GitHub Actions（可选，用于自动测试）

### 阶段 3：ClawHub 发布（可选）

- [ ] 注册 ClawHub 账号
- [ ] 提交技能审核
- [ ] 发布到技能市场

### 阶段 4：推广（可选）

- [ ] 在 OpenClaw 社区分享
- [ ] 编写使用教程
- [ ] 收集用户反馈

---

## 📝 待完成事项

### 代码层面

1. **更新占位符**
   - 将 `your-github-username` 替换为真实 GitHub 用户名
   - 更新所有文档中的链接

2. **添加 LICENSE**
   ```bash
   # 推荐 MIT 许可证
   curl -O https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/licenses/mit.txt
   mv mit.txt LICENSE
   ```

3. **添加 CHANGELOG.md**（可选）
   - 记录版本历史
   - 方便用户了解更新内容

### 文档层面

1. **更新 README.md**
   - 添加实际 GitHub 链接
   - 添加安装统计（发布后）
   - 添加使用示例截图

2. **创建示例视频/GIF**（可选）
   - 展示使用流程
   - 放在 README 中

### 测试层面

1. **添加自动化测试**
   ```bash
   # 创建 tests/ 目录
   # 添加 pytest 测试用例
   ```

2. **配置 CI/CD**（可选）
   - GitHub Actions
   - 自动测试和发布

---

## 🚀 快速执行命令

### 立即发布到 GitHub

```bash
cd /home/13928293596_wy/openclaw/workspace/skills/wechat-article-reader

# 1. 更新占位符（替换 YOUR_USERNAME）
sed -i 's/your-github-username/YOUR_USERNAME/g' package.json SKILL.md INSTALL.md

# 2. 初始化 Git
git init
git add -A
git commit -m "initial release: wechat-article-reader v1.0.0"

# 3. 创建 GitHub 仓库后，添加远程
git remote add origin https://github.com/YOUR_USERNAME/wechat-article-reader.git

# 4. 推送
git push -u origin main

# 5. 打标签
git tag -a "v1.0.0" -m "Initial release"
git push origin v1.0.0
```

### 发布到 ClawHub

```bash
# 确保已安装 Node.js
npx clawhub@latest publish

# 或运行发布脚本
bash publish.sh
```

---

## 📊 成功指标

- ✅ 其他用户可以一键安装
- ✅ 技能文档完整清晰
- ✅ 测试通过率 100%
- ✅ 无严重 Bug
- ✅ 用户反馈积极

---

## 🎉 总结

**当前状态**：技能已开发完成，测试通过，文档齐全

**下一步**：
1. 更新 GitHub 用户名
2. 创建 GitHub 仓库并推送
3. （可选）发布到 ClawHub

**预计时间**：30 分钟

---

**需要我继续执行吗？** 请告诉我你的 GitHub 用户名，我可以帮你：
1. 更新所有占位符
2. 初始化 Git 仓库
3. 准备推送

或者你可以手动执行上述命令。🦎
