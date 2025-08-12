#!/usr/bin/env python3
"""
优雅博客启动脚本
"""

import os
from app import app, db
from config import config

def create_app(config_name=None):
    """创建应用实例"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    with app.app_context():
        # 确保数据库表存在
        db.create_all()
        
        # 创建默认数据
        create_default_data()
    
    return app

def create_default_data():
    """创建默认数据"""
    from app import User, Category
    
    # 创建默认管理员账户
    if not User.query.filter_by(username='admin').first():
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        print("✅ 创建默认管理员账户: admin / admin123")
    
    # 创建默认分类
    if not Category.query.filter_by(slug='uncategorized').first():
        default_category = Category(
            name='未分类',
            slug='uncategorized',
            description='默认分类'
        )
        db.session.add(default_category)
        print("✅ 创建默认分类: 未分类")
    
    # 创建示例分类
    sample_categories = [
        {'name': '技术', 'slug': 'technology', 'description': '技术相关文章'},
        {'name': '生活', 'slug': 'life', 'description': '生活感悟'},
        {'name': '思考', 'slug': 'thinking', 'description': '深度思考'},
        {'name': '阅读', 'slug': 'reading', 'description': '读书笔记'},
        {'name': '写作', 'slug': 'writing', 'description': '写作技巧'}
    ]
    
    for cat_data in sample_categories:
        if not Category.query.filter_by(slug=cat_data['slug']).first():
            category = Category(**cat_data)
            db.session.add(category)
            print(f"✅ 创建分类: {cat_data['name']}")
    
    try:
        db.session.commit()
        print("✅ 默认数据创建完成")
    except Exception as e:
        print(f"❌ 创建默认数据时出错: {e}")
        db.session.rollback()

if __name__ == '__main__':
    # 创建应用
    app = create_app()
    
    # 获取配置
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = app.config.get('DEBUG', True)
    
    print(f"🚀 启动优雅博客...")
    print(f"📍 访问地址: http://{host}:{port}")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    print(f"👤 管理员账户: admin / admin123")
    print("=" * 50)
    
    # 启动应用
    app.run(
        host=host,
        port=port,
        debug=debug
    )
