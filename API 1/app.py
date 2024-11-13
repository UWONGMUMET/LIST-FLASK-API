from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Kantin(db.Model):
    __tablename__ = 'Kantin'
    id = db.Column(db.Integer, primary_key=True)
    makanan = db.Column(db.String(80), unique=True, nullable=False)
    minuman = db.Column(db.String(80), unique=True, nullable=False)
    harga = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'makanan': self.makanan, 'minuman': self.minuman, 'harga': self.harga}
    
with app.app_context():
    db.create_all()

@app.route('/kantin', methods = ['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

@app.route('/kantin', methods = ['POST'])
def create_data_kantin():
    try:
        data = request.get_json()
        new_kantin = Kantin(makanan = data['makanan'], minuman = data['minuman'], harga = data['harga'])
        db.session.add(new_kantin)
        db.session.commit()
        return make_response(jsonify({'message': 'data kantin created'}), 201)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to create data'}), 500)
    
@app.route('/kantin/<int:id>', methods=['GET'])
def get_data_kantin(id):
    try:
        kantin = Kantin.query.get(id)
        if kantin:
            return make_response(jsonify({'kantin_data': kantin.json()}), 200)
        return make_response(jsonify({'message': 'data kantin not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get data'}), 500)

@app.route('/kantin/<int:id>', methods=['PUT'])
def update_data_kantin(id):
    try:
        kantin = Kantin.query.get(id)
        if kantin:
            data = request.get_json()
            kantin.makanan = data['makanan']
            kantin.minuman = data['minuman']
            kantin.harga = data['harga']
            db.session.commit()
            return make_response(jsonify({'message': 'data kantin updated'}), 200)
        return make_response(jsonify({'message': 'data kantin not found'}), 404)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to update data'}), 500)

@app.route('/kantin/<int:id>', methods = ['DELETE'])
def delete_kantin_data(id):
    try:
        kantin = Kantin.query.get(id)
        if kantin:
            db.session.delete(kantin)
            db.session.commit()
            return make_response(jsonify({'message': 'data kantin deleted'}), 200)
        return make_response(jsonify({'message': 'data kantin not found'}), 404)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to delete data'}), 500)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the User API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)