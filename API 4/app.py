from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///museum_visitors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    visited_date = db.Column(db.String(255), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'age': self.age, 'visited_date': self.visited_date}

with app.app_context():
    db.create_all()

@app.route('/visitors', methods=['GET'])
def get_visitors():
    try:
        visitors = Visitor.query.all()
        return make_response(jsonify({'visitors': [visitor.json() for visitor in visitors]}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get visitors'}), 500)

@app.route('/visitors', methods=['POST'])
def create_visitor():
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('age') or not data.get('visited_date'):
            return make_response(jsonify({'message': 'Name, age, and visited date are required'}), 400)
        new_visitor = Visitor(name=data['name'], age=data['age'], visited_date=data['visited_date'])
        db.session.add(new_visitor)
        db.session.commit()
        return make_response(jsonify({'message': 'Visitor created successfully'}), 201)
    except SQLAlchemyError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to create visitor'}), 500)

@app.route('/visitors/<int:id>', methods=['GET'])
def get_visitor(id):
    try:
        visitor = Visitor.query.get(id)
        if visitor:
            return make_response(jsonify({'visitor': visitor.json()}), 200)
        return make_response(jsonify({'message': 'Visitor not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get visitor'}), 500)

@app.route('/visitors/<int:id>', methods=['PUT'])
def update_visitor(id):
    try:
        visitor = Visitor.query.get(id)
        if visitor:
            data = request.get_json()
            visitor.name = data['name']
            visitor.age = data['age']
            visitor.visited_date = data['visited_date']
            db.session.commit()
            return make_response(jsonify({'message': 'Visitor updated successfully'}), 200)
        return make_response(jsonify({'message': 'Visitor not found'}), 404)
    except SQLAlchemyError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to update visitor'}), 500)

@app.route('/visitors/<int:id>', methods=['DELETE'])
def delete_visitor(id):
    try:
        visitor = Visitor.query.get(id)
        if visitor:
            db.session.delete(visitor)
            db.session.commit()
            return make_response(jsonify({'message': 'Visitor deleted successfully'}), 200)
        return make_response(jsonify({'message': 'Visitor not found'}), 404)
    except SQLAlchemyError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to delete visitor'}), 500)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Museum Visitors API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)
