from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Kost(db.Model):
    __tablename__ = 'Kost'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), unique=True, nullable=False)
    umur = db.Column(db.Integer, nullable=False)
    daerah = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'id': self.id, 'nama': self.nama, 'umur': self.umur, 'daerah': self.daerah}
    
with app.app_context():
    db.create_all()

@app.route('/kost', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

@app.route('/kost', methods=['POST'])
def create_data_kost():
    try:
        data = request.get_json()
        new_kost = Kost(nama=data['nama'], umur=data['umur'], daerah=data['daerah'])
        db.session.add(new_kost)
        db.session.commit()
        return make_response(jsonify({'message': 'data kost created'}), 201)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating data kost'}), 500)

@app.route('/kost/<int:id>', methods=['GET'])
def get_data_kost(id):
    try:
        kost = Kost.query.get(id)
        if kost:
            return make_response(jsonify({'kost_data': kost.json()}), 200)
        return make_response(jsonify({'message': 'data kost not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': f'error getting kost data: {str(e)}'}), 500)
    
@app.route('/kost/<int:id>', methods=['PUT'])
def update_kost_data(id):
    try:
        kost = Kost.query.get(id)
        if kost:
            data = request.get_json()
            kost.nama = data['nama']
            kost.umur = data['umur']
            kost.daerah = data['daerah']
            db.session.commit()
            return make_response(jsonify({'message': 'data kost updated'}), 200)
        return make_response(jsonify({'message': 'data kost not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'error updating data kost: {str(e)}'}), 500)

@app.route('/kost/<int:id>', methods=['DELETE'])
def delete_kost_data(id):
    try:
        kost = Kost.query.get(id)
        if kost:
            db.session.delete(kost)
            db.session.commit()
            return make_response(jsonify({'message': 'data kost deleted'}), 200)
        return make_response(jsonify({'message': 'data kost not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'error deleting data kost: {str(e)}'}), 500)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the User API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)
