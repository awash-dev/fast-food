from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.product import Product, Category
from models.user import User
from utils.database import db
from utils.cloudinary_service import upload_image, delete_image
import os

products_bp = Blueprint('products', __name__)

def require_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    return None

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('category_id')
        query = Product.query.filter_by(is_available=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        products = query.all()
        return jsonify([product.to_dict() for product in products]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    if error := require_admin():
        return error
    
    try:
        # Check if image file is included
        image_file = request.files.get('image')
        image_url = None
        
        if image_file and image_file.filename != '':
            upload_result = upload_image(image_file, folder="fastfood-app/products")
            if 'error' in upload_result:
                return jsonify({'error': upload_result['error']}), 400
            image_url = upload_result['url']
        
        # Get other form data
        data = request.form.to_dict()
        
        product = Product(
            name=data['name'],
            description=data.get('description'),
            price=float(data['price']),
            image_url=image_url,
            category_id=int(data['category_id']),
            is_available=data.get('is_available', 'true').lower() == 'true'
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    if error := require_admin():
        return error
    
    try:
        product = Product.query.get_or_404(product_id)
        
        # Check if new image is uploaded
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            upload_result = upload_image(image_file, folder="fastfood-app/products")
            if 'error' in upload_result:
                return jsonify({'error': upload_result['error']}), 400
            product.image_url = upload_result['url']
        
        # Update other fields from form data
        data = request.form.to_dict()
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'is_available' in data:
            product.is_available = data['is_available'].lower() == 'true'
        if 'category_id' in data:
            product.category_id = int(data['category_id'])
        
        db.session.commit()
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    if error := require_admin():
        return error
    
    try:
        product = Product.query.get_or_404(product_id)
        
        # TODO: Optionally delete image from Cloudinary
        # if product.image_url:
        #     # Extract public_id from URL and delete
        #     pass
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    if error := require_admin():
        return error
    
    try:
        # Check if image file is included
        image_file = request.files.get('image')
        image_url = None
        
        if image_file and image_file.filename != '':
            upload_result = upload_image(image_file, folder="fastfood-app/categories")
            if 'error' in upload_result:
                return jsonify({'error': upload_result['error']}), 400
            image_url = upload_result['url']
        
        # Get other form data
        data = request.form.to_dict()
        
        category = Category(
            name=data['name'],
            description=data.get('description'),
            image_url=image_url
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400