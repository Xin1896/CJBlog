# 🚀 快速部署指南

## 📋 项目已推送到 GitHub

✅ 项目已成功推送到: [https://github.com/Xin1896/CJBlog.git](https://github.com/Xin1896/CJBlog.git)

## 🎯 部署到 Vercel 的步骤

### 1. 访问 Vercel
- 打开 [vercel.com](https://vercel.com)
- 使用 GitHub 账户登录

### 2. 导入项目
- 点击 "New Project"
- 选择 "Import Git Repository"
- 选择 `Xin1896/CJBlog` 仓库

### 3. 配置项目
- **Framework Preset**: 选择 "Other"
- **Root Directory**: 保持默认
- **Build Command**: 留空
- **Output Directory**: 留空
- **Install Command**: `pip install -r requirements.txt`

### 4. 环境变量设置
在项目设置中添加：

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database
FLASK_ENV=production
VERCEL_ENV=true
```

### 5. 数据库设置（推荐 Supabase）

1. 访问 [supabase.com](https://supabase.com)
2. 创建新项目
3. 在 SQL Editor 中运行数据库初始化脚本
4. 复制连接字符串到 Vercel 环境变量

### 6. 部署
- 点击 "Deploy"
- 等待部署完成
- 获得您的 Vercel 域名

## 🔗 重要链接

- **GitHub 仓库**: [https://github.com/Xin1896/CJBlog.git](https://github.com/Xin1896/CJBlog.git)
- **Vercel 平台**: [https://vercel.com](https://vercel.com)
- **Supabase**: [https://supabase.com](https://supabase.com)

## 📚 详细文档

查看 `VERCEL_DEPLOYMENT.md` 获取完整的部署指南和故障排除信息。

---

🎉 祝您部署顺利！
