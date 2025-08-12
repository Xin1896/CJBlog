# 优雅博客 - Elegant Blog

一个采用类似 Gates Notes 设计风格的 Flask 博客系统，注重优雅的用户体验和简洁的代码结构。

## ✨ 特性

- 🎨 **优雅设计**: 采用类似 Gates Notes 的现代简约设计风格
- 📱 **响应式布局**: 完美适配桌面端和移动端
- 🔐 **用户认证**: 完整的用户注册、登录和管理系统
- 📝 **文章管理**: 支持文章创建、编辑、删除和分类管理
- 🔍 **搜索功能**: 强大的文章搜索和分类浏览
- 🎯 **管理后台**: 直观的管理界面，轻松管理内容
- 🚀 **性能优化**: 图片懒加载、代码分割等性能优化
- 📊 **数据统计**: 文章阅读量统计和用户行为分析

## 🛠️ 技术栈

- **后端**: Flask 3.0 + SQLAlchemy + Flask-Login
- **前端**: 原生 HTML/CSS/JavaScript + 响应式设计
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **样式**: 自定义 CSS + CSS 变量 + Flexbox/Grid
- **字体**: Inter + Playfair Display (Google Fonts)

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd elegant-blog
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

5. **初始化数据库**
```bash
python run.py
```

6. **访问应用**
- 网站: http://localhost:5000
- 管理后台: http://localhost:5000/admin
- 默认管理员账户: `admin` / `admin123`

## 📁 项目结构

```
elegant-blog/
├── app.py                 # Flask 应用主文件
├── config.py             # 配置文件
├── run.py                # 启动脚本
├── requirements.txt      # 项目依赖
├── README.md            # 项目说明
├── static/              # 静态文件
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript 文件
│   ├── images/         # 图片资源
│   └── uploads/        # 用户上传文件
├── templates/           # 模板文件
│   ├── admin/          # 管理后台模板
│   ├── auth/           # 认证页面模板
│   ├── errors/         # 错误页面模板
│   ├── base.html       # 基础模板
│   ├── index.html      # 首页模板
│   ├── post.html       # 文章详情页
│   └── ...             # 其他页面模板
└── blog.db             # SQLite 数据库文件
```

## 🎨 设计特色

### 视觉设计
- **色彩搭配**: 采用深蓝灰色调，营造专业稳重的氛围
- **字体选择**: Inter 用于正文，Playfair Display 用于标题，提升可读性
- **间距布局**: 精心设计的间距和留白，让内容呼吸
- **阴影效果**: 适度的阴影层次，增强视觉深度

### 交互体验
- **平滑动画**: 所有交互都有流畅的过渡动画
- **悬停效果**: 丰富的悬停状态反馈
- **响应式反馈**: 即时的用户操作反馈
- **无障碍设计**: 考虑键盘导航和屏幕阅读器

## 🔧 配置说明

### 环境变量

```bash
# Flask 配置
SECRET_KEY=your-secret-key-here
FLASK_APP=app.py
FLASK_ENV=development

# 数据库配置
DATABASE_URL=sqlite:///blog.db

# 文件上传配置
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads
```

### 数据库配置

- **开发环境**: SQLite (默认)
- **生产环境**: PostgreSQL, MySQL 等
- **迁移**: 使用 Flask-Migrate 管理数据库版本

## 📱 响应式设计

- **移动优先**: 采用移动优先的设计理念
- **断点设计**: 
  - 移动端: < 768px
  - 平板端: 768px - 1024px
  - 桌面端: > 1024px
- **触摸友好**: 优化触摸设备的交互体验

## 🚀 部署指南

### 生产环境部署

1. **使用 Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

2. **使用 Docker**
```bash
docker build -t elegant-blog .
docker run -p 8000:8000 elegant-blog
```

3. **反向代理**
- 推荐使用 Nginx 作为反向代理
- 配置 SSL 证书确保 HTTPS 访问

### 性能优化

- **静态文件**: 使用 CDN 加速静态资源
- **数据库**: 配置数据库连接池和查询优化
- **缓存**: 实现 Redis 缓存提升响应速度
- **压缩**: 启用 Gzip 压缩减少传输大小

## 🔒 安全特性

- **CSRF 保护**: 所有表单都有 CSRF 令牌
- **SQL 注入防护**: 使用 SQLAlchemy ORM
- **XSS 防护**: 输入输出过滤和转义
- **密码安全**: 使用 Werkzeug 的密码哈希
- **会话安全**: 安全的 Cookie 配置

## 📊 功能模块

### 用户系统
- 用户注册和登录
- 密码重置
- 用户权限管理
- 个人资料管理

### 内容管理
- 文章创建和编辑
- 分类和标签管理
- 媒体文件上传
- 内容版本控制

### 管理后台
- 数据统计仪表板
- 用户管理
- 内容审核
- 系统设置

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 设计灵感来自 [Gates Notes](https://www.gatesnotes.com/)
- 字体来自 [Google Fonts](https://fonts.google.com/)
- 图标来自 [Feather Icons](https://feathericons.com/)

## 📞 联系我们

- 项目主页: [GitHub Repository]
- 问题反馈: [Issues]
- 邮箱: contact@elegantblog.com

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
