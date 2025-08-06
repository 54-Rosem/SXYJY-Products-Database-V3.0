from flask import Blueprint, request, jsonify, abort
from app.models import Product, Category
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@api_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    if not data or 'name' not in data:
        abort(400, 'Missing product name')
    category_ids = data.get('category_ids', [])
    # 处理分类
    categories = Category.query.filter(Category.id.in_(category_ids)).all()
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        ingredients=data.get('ingredients', ''),
        process=data.get('process', ''),
        efficacy=data.get('efficacy', ''),
        reference=data.get('reference', ''),
        size=data.get('size', ''),
        image_filename=data.get('image_filename', ''),
        categories = categories  # 关联分类
    )

    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    if not data:
        abort(400, 'No input data provided')

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.ingredients = data.get('ingredients', product.ingredients)
    product.process = data.get('process', product.process)
    product.efficacy = data.get('efficacy', product.efficacy)
    product.reference = data.get('reference', product.reference)
    product.size = data.get('size', product.size)
    product.image_filename = data.get('image_filename', product.image_filename)

    # 更新分类
    category_ids = data.get('category_ids')
    if category_ids is not None:
        categories = Category.query.filter(Category.id.in_(category_ids)).all()
        product.categories = categories

    db.session.commit()
    return jsonify(product.to_dict())

@api_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})