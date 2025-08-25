from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.product import Product, Category
from models.order import Order
from utils.database import db

admin_bp = Blueprint('admin', __name__)

def require_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    return None

@admin_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    if error := require_admin():
        return error
    
    try:
        data = request.get_json()
        product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            image_url=data.get('image_url'),
            category_id=data['category_id']
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'message': 'Product created successfully', 'product': product.to_dict()}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    if error := require_admin():
        return error
    
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'is_available' in data:
            product.is_available = data['is_available']
        if 'category_id' in data:
            product.category_id = data['category_id']
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    if error := require_admin():
        return error
    
    try:
        status = request.args.get('status')
        query = Order.query.order_by(Order.created_at.desc())
        
        if status:
            query = query.filter_by(status=status)
        
        orders = query.all()
        return jsonify([order.to_dict() for order in orders]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    if error := require_admin():
        return error
    
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        order.status = data['status']
        db.session.commit()
        
        return jsonify({'message': 'Order status updated successfully', 'order': order.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400