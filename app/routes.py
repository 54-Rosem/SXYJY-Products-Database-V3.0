from flask import Blueprint, render_template, current_app, send_from_directory, request
from app.models import Product, Category
from app import db         # 用于搜索时的 or 条件

bp = Blueprint('main', __name__)

@bp.route('/')
def product_list():
    # 1) 从 URL 查询参数中获取 q，如果不存在则默认为空字符串
    q = request.args.get('q', '').strip()

    if q:
        # 2) 如果 q 不为空，就根据产品名称或描述做模糊匹配
        products = Product.query.filter(
            db.or_(
                Product.name.ilike(f'%{q}%'),
                Product.description.ilike(f'%{q}%')
            )
        ).all()
    else:
        # 3) 如果 q 为空，则返回全部产品
        products = Product.query.all()

    # 4) 将当前 q 也传给模板，以便搜索框能保留输入内容
    return render_template('product_list.html', products=products, q=q)

@bp.route('/categories')
def categories():
    # 1. 定义两组分类名称
    form_names = ['饮料类','酸奶类','果冻类','糕点饼干类','糖果类','酒类','固体咖啡类',
                  '巧克力类','氮气饮类','冻干茶饮类','代用茶包类','其他类']
    efficacy_names = ['补气养血类','健脾养胃类','清咽类','解郁舒肝类','缓解疲劳类',
                      '安神助眠类','解酒类','明目类','增强免疫力类','清热生津类',
                      '美容养颜类','降尿酸类','减肥降脂类','降糖类','滋阴润燥类',
                      '祛湿排毒类','抗衰老类','驱寒暖胃类','待分类']

    # 2. 从数据库中分别查询这两组分类
    form_categories = Category.query.filter(Category.name.in_(form_names)).all()
    efficacy_categories = Category.query.filter(Category.name.in_(efficacy_names)).all()

    # 3. 渲染模板，传入两组列表
    return render_template(
        'categories.html',
        form_categories=form_categories,
        efficacy_categories=efficacy_categories
    )
@bp.route('/category/<int:category_id>')
def products_by_category(category_id):
    # 根据 ID 获取分类对象，找不到就返回 404
    cat = Category.query.get_or_404(category_id)
    # 通过 backref 获取该分类关联的所有产品
    products = cat.products.all()
    # 传入 product_list 模板，并带上当前分类以方便前端显示标题或高亮
    return render_template(
        'product_list.html',
        products=products,
        current_category=cat,
        q=''   # 清空搜索框
    )

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    p = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=p)

@bp.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
