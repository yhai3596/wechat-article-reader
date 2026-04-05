# 🔑 添加 SSH Key 到 GitHub

## SSH 公钥

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDCQaYqN7Cpeb2XrPUANphQbcUVTyv5QW+/UFY9u5mkq yhai3596@users.noreply.github.com
```

## 添加步骤

### 1. 复制公钥

点击上方的复制按钮，或运行：
```bash
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard
```

### 2. 在 GitHub 添加 SSH Key

1. **访问**: https://github.com/settings/keys

2. **点击**: "New SSH key" 或 "Add SSH key"

3. **填写信息**:
   - **Title**: `OpenClaw Server`（或任意名称）
   - **Key type**: ✅ Authentication Key
   - **Key**: 粘贴上面的公钥

4. **点击**: "Add SSH key"

### 3. 验证连接

添加完成后，运行：
```bash
ssh -T git@github.com
```

期望输出：
```
Hi yhai3596! You've successfully authenticated, but GitHub does not provide shell access.
```

### 4. 切换为 SSH 方式推送

```bash
cd /home/13928293596_wy/openclaw/workspace/skills/wechat-article-reader

# 移除 HTTPS remote
git remote remove origin

# 添加 SSH remote
git remote add origin git@github.com:yhai3596/wechat-article-reader.git

# 推送
git push -u origin main --tags
```

## 完成！

推送成功后，访问：https://github.com/yhai3596/wechat-article-reader

---

**添加完 SSH key 后，告诉我，我会继续执行推送！**
