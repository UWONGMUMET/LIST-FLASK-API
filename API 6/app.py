from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///restaurant_customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    visit_date =  db.Column(db.String(255), nullable=False)
    table_number = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'visit_date': self.visit_date,
            'table_number': self.table_number
        }

with app.app_context():
    db.create_all()

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = Customer.query.all()
        return make_response(jsonify({'customers': [customer.json() for customer in customers]}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get customers'}), 500)

@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('phone') or not data.get('visit_date') or not data.get('table_number'):
            return make_response(jsonify({'message': 'Name, phone, visit date, and table number are required'}), 400)
        new_customer = Customer(
            name=data['name'],
            phone=data['phone'],
            visit_date=data['visit_date'],
            table_number=data['table_number']
        )
        db.session.add(new_customer)
        db.session.commit()
        return make_response(jsonify({'message': 'Customer created successfully'}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to create customer', 'error': str(e)}), 500)
    
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        customer = Customer.query.get(id)
        if customer:
            return make_response(jsonify({'message': customer.json()}), 200)
        return make_response(jsonify({'message': 'Customer not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Failed to get customer', 'error': str(e)}), 500)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer = Customer.query.get(id)
        if customer:
            data = request.get_json()
            customer.name = data['name']
            customer.phone = data['phone']
            customer.visit_date = data['visit_date']
            customer.table_number = data['table_number']
            db.session.commit()
            return make_response(jsonify({'message': 'Customer updated successfully'}), 200)
        return make_response(jsonify({'message': 'Customer not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to update customer', 'error': str(e)}), 500)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get(id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return make_response(jsonify({'message': 'Customer deleted successfully'}), 200)
        return make_response(jsonify({'message': 'Customer not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to delete customer', 'error': str(e)}), 500)
        
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Restaurant Customers API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)