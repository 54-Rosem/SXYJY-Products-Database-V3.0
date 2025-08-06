from app import db

# 关联表，实现产品和分类的多对多关系
product_category = db.Table('product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)  # 分类名称，如“饮料类”、“补气类”等

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'
    #__tablename__ 是用来指定模型类对应的数据库表的名称。这里我们将其命名为 'products'，即数据库中的表名将是 products。
    id = db.Column(db.Integer, primary_key=True)
    #id 是表的主键，primary_key=True 表示这是主键字段。每个产品都有一个唯一的 id，用于唯一标识该产品。
    #db.Integer 表示 id 字段的数据类型为整数。
    name = db.Column(db.String(128), nullable=False)
    #name 字段表示产品的名称，类型是字符串，最大长度为 128 个字符。
    #nullable=False 表示该字段是必填的，不能为 NULL。
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    #ingredients 字段用于存储配料，使用 Text 类型存储长文本。
    #nullable=False 表示该字段是必填的。
    process = db.Column(db.Text, nullable=True)
    #process 字段用于存储工艺过程。它的类型是 Text，适合存储较长的文本信息，且它是可选字段（nullable=True）。
    efficacy = db.Column(db.Text, nullable=True)
    #efficacy 字段用于存储产品的功效，同样是可选字段，类型为 Text。
    image_filename = db.Column(db.String(128), nullable=True)
    #image_filename 字段用于存储图片文件的名称或路径。它是一个可选字段，类型为字符串（最多 128 个字符）。
    reference = db.Column(db.Text, nullable=True)
    size = db.Column(db.Text, nullable=True)

    categories = db.relationship('Category', secondary=product_category, backref=db.backref('products', lazy='dynamic'))
    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ingredients': self.ingredients,
            'process': self.process,
            'efficacy': self.efficacy,
            'image_filename': self.image_filename,
            'reference': self.reference,
            'size': self.size,
            # categories 字段是一个列表，包含该产品关联的所有分类的名称
            'categories': [category.name for category in self.categories]
        }