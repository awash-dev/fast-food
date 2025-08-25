from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order, OrderItem
from models.product import Product
from utils.database import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Calculate total amount and validate products
        total_amount = 0
        order_items = []
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product or not product.is_available:
                return jsonify({'error': f'Product {item["product_id"]} not available'}), 400
            
            item_total = product.price * item['quantity']
            total_amount += item_total
            
            order_items.append(OrderItem(
                product_id=product.id,
                quantity=item['quantity'],
                price=product.price
            ))
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            delivery_address=data['delivery_address'],
            phone=data['phone'],
            notes=data.get('notes'),
            items=order_items
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_orders():
    try:
        user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return jsonify([order.to_dict() for order in orders]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id)
        
        # Check if user owns the order or is admin
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(order.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404