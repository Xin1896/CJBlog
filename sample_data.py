#!/usr/bin/env python3
"""
示例数据生成脚本
用于创建示例文章和分类数据
"""

from app import app, db, User, Category, Post
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_data():
    """创建示例数据"""
    with app.app_context():
        print("🚀 开始创建示例数据...")
        
        # 创建示例分类
        categories_data = [
            {'name': '技术', 'slug': 'technology', 'description': '技术相关文章，包括编程、开发、工具等'},
            {'name': '生活', 'slug': 'life', 'description': '生活感悟、日常思考、个人经历'},
            {'name': '思考', 'slug': 'thinking', 'description': '深度思考、哲学思辨、人生感悟'},
            {'name': '阅读', 'slug': 'reading', 'description': '读书笔记、书评、阅读心得'},
            {'name': '写作', 'slug': 'writing', 'description': '写作技巧、创作心得、文字艺术'}
        ]
        
        categories = {}
        for cat_data in categories_data:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                category = Category(**cat_data)
                db.session.add(category)
                categories[cat_data['slug']] = category
                print(f"✅ 创建分类: {cat_data['name']}")
        
        # 创建示例用户
        if not User.query.filter_by(username='demo').first():
            demo_user = User(
                username='demo',
                email='demo@example.com',
                password_hash=generate_password_hash('demo123'),
                is_admin=False
            )
            db.session.add(demo_user)
            print("✅ 创建示例用户: demo / demo123")
        
        # 创建示例文章
        sample_posts = [
            {
                'title': 'Flask 开发最佳实践',
                'excerpt': '分享在 Flask 开发过程中的一些最佳实践和经验总结，帮助开发者构建更好的应用。',
                'content': '''
# Flask 开发最佳实践

Flask 是一个轻量级的 Python Web 框架，它提供了灵活性，但也需要开发者自己做出很多选择。在这篇文章中，我将分享一些在 Flask 开发过程中的最佳实践。

## 1. 项目结构

良好的项目结构是成功的基础。推荐使用以下结构：

```
myapp/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── templates/
├── config.py
├── requirements.txt
└── run.py
```

## 2. 配置管理

使用配置类来管理不同环境的配置：

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

## 3. 数据库模型

使用 SQLAlchemy 来定义数据模型，并遵循命名约定：

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## 4. 错误处理

实现全局错误处理来提供更好的用户体验：

```python
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
```

## 5. 安全性考虑

- 使用 CSRF 保护
- 验证和清理用户输入
- 使用安全的密码哈希
- 实现适当的访问控制

## 总结

Flask 是一个强大的框架，但需要开发者自己做出很多架构决策。遵循这些最佳实践可以帮助你构建更可维护、更安全的 Flask 应用。

记住，最佳实践不是一成不变的，要根据项目的具体需求来调整。
                ''',
                'category_slug': 'technology',
                'is_published': True
            },
            {
                'title': '生活中的小确幸',
                'excerpt': '记录生活中那些微小但美好的瞬间，感受平凡日子里的温暖与感动。',
                'content': '''
# 生活中的小确幸

生活中总有一些微小但美好的瞬间，它们像星星一样点缀着我们的日常，让我们在忙碌的生活中感受到温暖与感动。

## 清晨的第一缕阳光

每天早上，当第一缕阳光透过窗帘洒进房间时，那种温暖的感觉总是让人心情愉悦。新的一天开始了，充满了无限的可能性。

## 一杯热茶的温暖

在寒冷的冬日，捧着一杯热茶，看着窗外的雪花飘落，这种宁静的时刻让人感到内心的平静与满足。

## 朋友间的简单问候

收到朋友的一句简单问候，或者是一个温暖的拥抱，这些看似平常的互动，却能给人带来巨大的力量。

## 完成一个小目标的成就感

无论是完成一项工作任务，还是学会一个新的技能，那种成就感总是让人感到满足和快乐。

## 与家人共度的时光

与家人一起吃饭、聊天、看电视，这些平凡的时光却是最珍贵的财富。

## 总结

生活中的小确幸往往隐藏在日常的细节中，只要我们用心去感受，就能发现生活中的美好。让我们珍惜这些美好的瞬间，让生活变得更加美好。
                ''',
                'category_slug': 'life',
                'is_published': True
            },
            {
                'title': '深度思考的力量',
                'excerpt': '探讨深度思考在现代社会中的重要性，以及如何培养深度思考的能力。',
                'content': '''
# 深度思考的力量

在这个信息爆炸的时代，我们每天都被大量的信息包围，但真正有价值的思考却越来越少。深度思考成为了一种稀缺的能力，也是一种重要的竞争力。

## 什么是深度思考？

深度思考是指对问题进行深入分析，透过现象看本质，形成独立见解的思考过程。它不同于浅层思考，需要时间、专注和持续的努力。

## 深度思考的重要性

### 1. 提升决策质量

深度思考能帮助我们更好地分析问题，做出更明智的决策。在复杂的情况下，浅层思考往往会导致错误的判断。

### 2. 增强创新能力

创新往往来自于对问题的深入思考。只有深入理解问题的本质，才能找到创新的解决方案。

### 3. 提高学习效率

深度思考能帮助我们更好地理解知识，建立知识之间的联系，形成系统的知识体系。

## 如何培养深度思考能力？

### 1. 留出思考时间

每天留出专门的时间进行思考，远离干扰，专注于问题的深入分析。

### 2. 多问为什么

不要满足于表面的答案，多问几个为什么，深入挖掘问题的根源。

### 3. 记录思考过程

将思考过程记录下来，有助于理清思路，发现思考中的漏洞。

### 4. 与他人交流

与他人交流想法，听取不同的观点，能帮助我们更全面地思考问题。

## 总结

深度思考是一种需要培养的能力，它需要时间、耐心和持续的努力。在这个快节奏的时代，保持深度思考的能力，将是我们最重要的竞争优势之一。
                ''',
                'category_slug': 'thinking',
                'is_published': True
            },
            {
                'title': '《百年孤独》读后感',
                'excerpt': '分享阅读马尔克斯《百年孤独》的深刻感悟，探讨魔幻现实主义文学的魅力。',
                'content': '''
# 《百年孤独》读后感

《百年孤独》是加西亚·马尔克斯的代表作，也是魔幻现实主义文学的经典之作。这部作品以其独特的叙事方式和深刻的主题内涵，给我留下了深刻的印象。

## 魔幻现实主义的魅力

《百年孤独》最吸引人的地方在于它将现实与魔幻完美地结合在一起。在马尔克斯的笔下，飞升的美丽女子、会说话的鬼魂、持续四年的大雨，这些看似荒诞的情节却蕴含着深刻的现实意义。

## 时间的循环与孤独

小说以布恩迪亚家族的兴衰为主线，展现了时间的循环性和人类永恒的孤独。每一代人都重复着相似的命运，这种循环让人感到深深的无力感和孤独感。

## 家族命运的象征

布恩迪亚家族的历史实际上是人类历史的缩影。从最初的开拓精神，到后来的衰落和消亡，反映了人类文明发展的普遍规律。

## 语言的魔力

马尔克斯的语言具有一种特殊的魔力，他能够用最朴实的语言描述最神奇的事情，让读者在现实与魔幻之间自由穿梭。

## 对现实的反思

虽然《百年孤独》充满了魔幻色彩，但它实际上是对拉美现实的深刻反思。通过魔幻的手法，马尔克斯揭示了拉美社会的各种问题和矛盾。

## 总结

《百年孤独》是一部值得反复阅读的经典之作。它不仅让我们领略了魔幻现实主义文学的魅力，更让我们思考人类命运、时间本质等深刻的哲学问题。
                ''',
                'category_slug': 'reading',
                'is_published': True
            },
            {
                'title': '写作的艺术与技巧',
                'excerpt': '探讨写作的艺术性，分享实用的写作技巧，帮助提升写作水平。',
                'content': '''
# 写作的艺术与技巧

写作是一门艺术，也是一种技能。它需要天赋，更需要后天的学习和练习。在这篇文章中，我将分享一些关于写作的心得和技巧。

## 写作的本质

写作的本质是思想的表达和情感的传递。好的写作应该能够清晰地表达思想，深刻地触动读者的情感。

## 写作的基本要素

### 1. 主题明确

每篇文章都应该有一个明确的主题，所有的内容都应该围绕这个主题展开。

### 2. 结构清晰

文章的结构应该清晰明了，让读者能够轻松地跟随作者的思路。

### 3. 语言生动

生动的语言能够增强文章的感染力，让读者更容易产生共鸣。

### 4. 逻辑严密

文章的逻辑应该严密，避免前后矛盾，让读者信服。

## 写作技巧

### 1. 开头要吸引人

文章的开头决定了读者是否愿意继续阅读。一个好的开头应该能够立即抓住读者的注意力。

### 2. 细节要具体

具体的细节能够让文章更加生动，让读者有身临其境的感觉。

### 3. 结尾要有力

文章的结尾应该给读者留下深刻的印象，让读者在合上书页后仍然回味无穷。

### 4. 修改要仔细

好的文章是改出来的。写完初稿后，要仔细修改，不断完善。

## 写作的练习方法

### 1. 每天写作

养成每天写作的习惯，哪怕只是写几句话，也能帮助提升写作水平。

### 2. 广泛阅读

阅读是写作的基础。通过阅读优秀的作品，我们可以学习到很多写作技巧。

### 3. 模仿练习

选择自己喜欢的作家，模仿他们的写作风格，这是一种很好的学习方式。

### 4. 接受反馈

虚心接受他人的反馈，从中发现自己的不足，不断改进。

## 总结

写作是一门需要不断练习的艺术。通过掌握基本的技巧，加上持续的练习，我们都能成为更好的写作者。记住，写作没有捷径，只有通过不断的努力，才能写出真正优秀的作品。
                ''',
                'category_slug': 'writing',
                'is_published': True
            }
        ]
        
        # 创建文章
        for post_data in sample_posts:
            if not Post.query.filter_by(title=post_data['title']).first():
                category = categories.get(post_data['category_slug'])
                if category:
                    # 随机生成创建时间（过去30天内）
                    days_ago = random.randint(0, 30)
                    created_at = datetime.utcnow() - timedelta(days=days_ago)
                    
                    post = Post(
                        title=post_data['title'],
                        slug=post_data['title'].lower().replace(' ', '-').replace('《', '').replace('》', ''),
                        content=post_data['content'],
                        excerpt=post_data['excerpt'],
                        category_id=category.id,
                        user_id=1,  # 假设管理员用户ID为1
                        is_published=post_data['is_published'],
                        created_at=created_at,
                        updated_at=created_at,
                        view_count=random.randint(10, 500)
                    )
                    db.session.add(post)
                    print(f"✅ 创建文章: {post_data['title']}")
        
        try:
            db.session.commit()
            print("🎉 示例数据创建完成！")
            print("📊 数据统计:")
            print(f"   - 分类: {Category.query.count()} 个")
            print(f"   - 用户: {User.query.count()} 个")
            print(f"   - 文章: {Post.query.count()} 篇")
        except Exception as e:
            print(f"❌ 创建示例数据时出错: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_sample_data()
