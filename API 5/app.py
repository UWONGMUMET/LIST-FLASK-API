from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///cake_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CakeOrder(db.Model):
    __tablename__ = 'cake_orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    order_date = db.Column(db.String(255), nullable=False)
    cake_type = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'phone': self.phone,
            'order_date': self.order_date,
            'cake_type': self.cake_type,
            'quantity': self.quantity
        }

with app.app_context():
    db.create_all()

@app.route('/cake_orders', methods=['GET'])
def get_orders():
    try:
        orders = CakeOrder.query.all()
        return make_response(jsonify({'orders': [order.json() for order in orders]}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get cake orders'}), 500)

@app.route('/cake_orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data.get('customer_name') or not data.get('phone') or not data.get('order_date') or not data.get('cake_type') or not data.get('quantity'):
            return make_response(jsonify({'message': 'Customer name, phone, order date, cake type, and quantity are required'}), 400)
        
        new_order = CakeOrder(
            customer_name=data['customer_name'],
            phone=data['phone'],
            order_date=data['order_date'],
            cake_type=data['cake_type'],
            quantity=data['quantity']
        )
        
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify({'message': 'Cake order created successfully'}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to create cake order', 'error': str(e)}), 500)

@app.route('/cake_orders/<int:id>', methods=['GET'])
def get_order(id):
    try:
        order = CakeOrder.query.get(id)
        if order:
            return make_response(jsonify({'order': order.json()}), 200)
        return make_response(jsonify({'message': 'Order not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Failed to get cake order', 'error': str(e)}), 500)

@app.route('/cake_orders/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        order = CakeOrder.query.get(id)
        if order:
            data = request.get_json()
            order.customer_name = data['customer_name']
            order.phone = data['phone']
            order.order_date = data['order_date']
            order.cake_type = data['cake_type']
            order.quantity = data['quantity']
            db.session.commit()
            return make_response(jsonify({'message': 'Cake order updated successfully'}), 200)
        return make_response(jsonify({'message': 'Order not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to update cake order', 'error': str(e)}), 500)

@app.route('/cake_orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = CakeOrder.query.get(id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return make_response(jsonify({'message': 'Cake order deleted successfully'}), 200)
        return make_response(jsonify({'message': 'Order not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to delete cake order', 'error': str(e)}), 500)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Cake Orders API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)