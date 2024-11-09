from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), unique=True, nullable=False)
    fakultas = db.Column(db.String(80), unique=True, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'nama': self.nama, 'fakultas': self.fakultas, 'semester': self.semester}
    
with app.app_context():
    db.create_all()

@app.route('/mahasiswa', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

@app.route('/mahasiswa', methods=['POST'])
def create_mahasiswa_data():
    try:
        data = request.get_json()
        new_mahasiswa = Mahasiswa(nama=data['nama'], fakultas=data['fakultas'], semester=data['semester'])
        db.session.add(new_mahasiswa)
        db.session.commit()
        return make_response(jsonify({'message': 'mahasiswa_data created'}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'error creating mahasiswa_data: {str(e)}'}), 500)

@app.route('/mahasiswa/<int:id>', methods=['GET'])
def get_mahasiswa_data(id):
    try:
        mahasiswa = Mahasiswa.query.get(id)
        if mahasiswa:
            return make_response(jsonify({'mahasiswa_data': mahasiswa.json()}), 200)
        return make_response(jsonify({'message': 'mahasiswa_data not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': f'error getting mahasiswa_data: {str(e)}'}), 500)

@app.route('/mahasiswa/<int:id>', methods=['PUT'])
def update_mahasiswa_data(id):
    try:
        mahasiswa = Mahasiswa.query.get(id)
        if mahasiswa:
            data = request.get_json()
            mahasiswa.nama = data['nama']
            mahasiswa.fakultas = data['fakultas']
            mahasiswa.semester = data['semester']
            db.session.commit()
            return make_response(jsonify({'message': 'mahasiswa_data updated'}), 200)
        return make_response(jsonify({'message': 'mahasiswa_data not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'error updating mahasiswa_data: {str(e)}'}), 500)

@app.route('/mahasiswa/<int:id>', methods=['DELETE'])
def delete_mahasiswa_data(id):
    try:
        mahasiswa = Mahasiswa.query.get(id)
        if mahasiswa:
            db.session.delete(mahasiswa)
            db.session.commit()
            return make_response(jsonify({'message': 'mahasiswa_data deleted'}), 200)
        return make_response(jsonify({'message': 'mahasiswa_data not found'}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'error deleting mahasiswa_data: {str(e)}'}), 500)
    
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the User API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)