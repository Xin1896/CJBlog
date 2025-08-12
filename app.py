from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# Vercel 环境检测
if os.environ.get('VERCEL_ENV'):
    # Vercel 生产环境
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vercel-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # Vercel 使用临时目录
else:
    # 本地开发环境
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面。'

# 数据库模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    posts = db.relationship('Post', backref='category', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_tags', backref='tags')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    view_count = db.Column(db.Integer, default=0)

# 多对多关系表
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 路由
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    categories = Category.query.all()
    featured_posts = Post.query.filter_by(is_published=True).order_by(Post.view_count.desc()).limit(3).all()
    
    return render_template('index.html', posts=posts, categories=categories, featured_posts=featured_posts)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.view_count += 1
    db.session.commit()
    
    # 获取相关文章
    related_posts = Post.query.filter(
        Post.category_id == post.category_id,
        Post.id != post.id,
        Post.is_published == True
    ).limit(3).all()
    
    return render_template('post.html', post=post, related_posts=related_posts)

@app.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=category.id, is_published=True).order_by(
        Post.created_at.desc()).paginate(page=page, per_page=6, error_out=False)
    
    return render_template('category.html', category=category, posts=posts)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        posts = Post.query.filter(
            Post.title.contains(query) | Post.content.contains(query),
            Post.is_published == True
        ).order_by(Post.created_at.desc()).all()
    else:
        posts = []
    
    return render_template('search.html', posts=posts, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# 管理路由
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    
    posts_count = Post.query.count()
    users_count = User.query.count()
    categories_count = Category.query.count()
    
    return render_template('admin/dashboard.html', 
                         posts_count=posts_count,
                         users_count=users_count,
                         categories_count=categories_count)

@app.route('/admin/posts')
@login_required
def admin_posts():
    if not current_user.is_admin:
        abort(403)
    
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if not current_user.is_admin:
        abort(403)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        excerpt = request.form['excerpt']
        category_id = request.form['category_id']
        is_published = 'is_published' in request.form
        
        # 生成 slug
        from slugify import slugify
        slug = slugify(title)
        
        post = Post(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            category_id=category_id,
            is_published=is_published,
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('文章创建成功！', 'success')
        return redirect(url_for('admin_posts'))
    
    categories = Category.query.all()
    return render_template('admin/new_post.html', categories=categories)

@app.route('/admin/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    if not current_user.is_admin:
        abort(403)
    
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.excerpt = request.form['excerpt']
        post.category_id = request.form['category_id']
        post.is_published = 'is_published' in request.form
        
        db.session.commit()
        flash('文章更新成功！', 'success')
        return redirect(url_for('admin_posts'))
    
    categories = Category.query.all()
    return render_template('admin/edit_post.html', post=post, categories=categories)

@app.route('/admin/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    if not current_user.is_admin:
        abort(403)
    
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    flash('文章删除成功！', 'success')
    return redirect(url_for('admin_posts'))

# 认证路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return render_template('auth/register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Vercel 入口点
@app.route('/api/hello')
def hello():
    return {'message': 'Hello from Vercel!'}

# 健康检查端点
@app.route('/health')
def health():
    return {'status': 'healthy', 'message': '优雅博客运行正常'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员账户
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            
            # 创建默认分类
            default_category = Category(
                name='未分类',
                slug='uncategorized',
                description='默认分类'
            )
            db.session.add(default_category)
            db.session.commit()
    
    app.run(debug=True)
