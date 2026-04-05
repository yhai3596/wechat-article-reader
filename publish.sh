#!/bin/bash
# 发布脚本 - 将技能发布到 GitHub 和 ClawHub

set -e

echo "🚀 开始发布 wechat-article-reader 技能..."

# 配置
REPO_NAME="wechat-article-reader"
GITHUB_USER="yhai3596"  # GitHub username
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 技能目录：$SKILL_DIR"

# 检查必要文件
echo "📋 检查必要文件..."
REQUIRED_FILES=("SKILL.md" "README.md" "wechat_reader.py" "tool.py" "package.json" "INSTALL.md")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$SKILL_DIR/$file" ]; then
        echo "❌ 缺少必要文件：$file"
        exit 1
    fi
done
echo "✅ 所有必要文件存在"

# 检查 Git
echo "🔍 检查 Git 状态..."
cd "$SKILL_DIR"

if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi

git status

# 添加所有文件
echo "📝 添加文件..."
git add -A

# 提交
echo "💾 提交更改..."
read -p "输入版本号 (例如 1.0.0): " VERSION
git commit -m "release: v$VERSION - 微信公众号文章读取技能" || echo "没有更改需要提交"

# 打标签
echo "🏷️  创建标签..."
git tag -a "v$VERSION" -m "Release v$VERSION"

# 推送到 GitHub
echo "📤 推送到 GitHub..."
read -p "是否推送到 GitHub? (y/n): " PUSH_TO_GITHUB
if [ "$PUSH_TO_GITHUB" = "y" ]; then
    git push origin main --tags
    echo "✅ 已推送到 GitHub"
    echo "🌐 查看：https://github.com/$GITHUB_USER/$REPO_NAME"
else
    echo "⏭️  跳过 GitHub 推送"
fi

# 发布到 ClawHub（可选）
echo ""
echo "📦 发布到 ClawHub（可选）..."
read -p "是否发布到 ClawHub? (y/n): " PUBLISH_CLAWHUB
if [ "$PUBLISH_CLAWHUB" = "y" ]; then
    if command -v npx &> /dev/null; then
        echo "🚀 发布到 ClawHub..."
        npx clawhub@latest publish
        echo "✅ 已发布到 ClawHub"
    else
        echo "⚠️  未找到 npx，跳过 ClawHub 发布"
        echo "💡 安装 Node.js 以使用 ClawHub: https://nodejs.org"
    fi
fi

echo ""
echo "🎉 发布完成！"
echo ""
echo "📚 下一步："
echo "1. 在 GitHub 上创建仓库（如果还没有）"
echo "2. 更新 README.md 中的 GitHub 链接"
echo "3. 分享给其他小龙虾！"
echo ""
echo "🔗 安装命令："
echo "   npx clawhub@latest install $REPO_NAME"
echo ""
