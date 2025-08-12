# Vercel 部署指南

## 🚀 部署到 Vercel

本指南将帮助您将优雅博客部署到 Vercel 平台。

## 📋 前置要求

1. **Vercel 账户**: 在 [vercel.com](https://vercel.com) 注册账户
2. **GitHub 仓库**: 将项目推送到 GitHub
3. **数据库**: 准备 PostgreSQL 数据库（推荐使用 Supabase 或 Railway）

## 🔧 部署步骤

### 1. 准备项目

确保项目包含以下文件：
- `vercel.json` - Vercel 配置文件
- `requirements.txt` - Python 依赖
- `app.py` - Flask 应用主文件

### 2. 推送到 GitHub

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: 优雅博客项目"

# 添加远程仓库
git remote add origin https://github.com/Xin1896/CJBlog.git

# 推送到 GitHub
git push -u origin main
```

### 3. 在 Vercel 上部署

1. **登录 Vercel**: 访问 [vercel.com](https://vercel.com) 并登录
2. **导入项目**: 点击 "New Project"
3. **选择仓库**: 选择您的 GitHub 仓库
4. **配置项目**:
   - Framework Preset: 选择 "Other"
   - Root Directory: 保持默认
   - Build Command: 留空
   - Output Directory: 留空
   - Install Command: `pip install -r requirements.txt`

### 4. 环境变量配置

在 Vercel 项目设置中添加以下环境变量：

```bash
# 必需的环境变量
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database

# 可选的环境变量
FLASK_ENV=production
VERCEL_ENV=true
```

### 5. 数据库设置

#### 使用 Supabase（推荐）

1. 访问 [supabase.com](https://supabase.com)
2. 创建新项目
3. 在 SQL Editor 中运行以下 SQL：

```sql
-- 创建用户表
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建分类表
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- 创建文章表
CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    featured_image VARCHAR(200),
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES "user"(id) NOT NULL,
    category_id INTEGER REFERENCES category(id) NOT NULL,
    view_count INTEGER DEFAULT 0
);

-- 创建标签表
CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

-- 创建文章标签关联表
CREATE TABLE post_tags (
    post_id INTEGER REFERENCES post(id),
    tag_id INTEGER REFERENCES tag(id),
    PRIMARY KEY (post_id, tag_id)
);

-- 插入默认数据
INSERT INTO "user" (username, email, password_hash, is_admin) 
VALUES ('admin', 'admin@example.com', 'pbkdf2:sha256:600000$...', true);

INSERT INTO category (name, slug, description) VALUES 
('未分类', 'uncategorized', '默认分类'),
('技术', 'technology', '技术相关文章'),
('生活', 'life', '生活感悟'),
('思考', 'thinking', '深度思考'),
('阅读', 'reading', '读书笔记'),
('写作', 'writing', '写作技巧');
```

4. 复制数据库连接字符串到 Vercel 环境变量

#### 使用 Railway

1. 访问 [railway.app](https://railway.app)
2. 创建新项目
3. 添加 PostgreSQL 服务
4. 复制连接字符串到 Vercel

### 6. 部署配置

#### vercel.json 说明

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

- `builds`: 指定构建配置
- `routes`: 路由重写规则
- `env`: 环境变量设置

## 🧪 测试部署

部署完成后，测试以下端点：

- **首页**: `https://your-project.vercel.app/`
- **健康检查**: `https://your-project.vercel.app/health`
- **API 测试**: `https://your-project.vercel.app/api/hello`

## 🔍 常见问题

### 1. 数据库连接错误

**症状**: 应用启动时出现数据库连接错误

**解决方案**:
- 检查 `DATABASE_URL` 环境变量是否正确
- 确保数据库服务正在运行
- 验证数据库凭据

### 2. 静态文件不加载

**症状**: CSS 和 JavaScript 文件无法加载

**解决方案**:
- 确保 `static` 文件夹在项目根目录
- 检查文件路径是否正确
- 验证 Vercel 构建配置

### 3. 路由不工作

**症状**: 某些页面返回 404 错误

**解决方案**:
- 检查 `vercel.json` 中的路由配置
- 确保所有模板文件都存在
- 验证 Flask 路由定义

### 4. 环境变量问题

**症状**: 应用无法读取环境变量

**解决方案**:
- 在 Vercel 项目设置中添加环境变量
- 重启部署
- 检查变量名是否正确

## 📊 性能优化

### 1. 数据库优化

- 使用连接池
- 添加适当的索引
- 优化查询语句

### 2. 缓存策略

- 实现 Redis 缓存
- 使用 CDN 加速静态文件
- 页面级缓存

### 3. 图片优化

- 使用 WebP 格式
- 实现图片懒加载
- 压缩图片文件

## 🔒 安全考虑

### 1. 环境变量

- 不要在代码中硬编码敏感信息
- 使用强密码和密钥
- 定期轮换密钥

### 2. 数据库安全

- 使用 SSL 连接
- 限制数据库访问权限
- 定期备份数据

### 3. 应用安全

- 启用 HTTPS
- 实现 CSRF 保护
- 验证用户输入

## 📈 监控和维护

### 1. 性能监控

- 使用 Vercel Analytics
- 监控数据库性能
- 跟踪错误日志

### 2. 定期维护

- 更新依赖包
- 检查安全漏洞
- 优化数据库查询

### 3. 备份策略

- 定期备份数据库
- 保存重要配置文件
- 建立恢复流程

## 🎯 下一步

部署成功后，您可以：

1. **自定义域名**: 在 Vercel 中配置自定义域名
2. **SSL 证书**: 自动获得 HTTPS 支持
3. **CDN 加速**: 享受全球 CDN 加速
4. **自动部署**: 每次推送代码自动部署
5. **预览部署**: 为每个 PR 创建预览环境

## 📞 获取帮助

如果遇到问题：

1. 查看 [Vercel 文档](https://vercel.com/docs)
2. 检查 [Flask 文档](https://flask.palletsprojects.com/)
3. 在 GitHub 上提交 Issue
4. 查看 Vercel 部署日志

---

祝您部署顺利！🚀
