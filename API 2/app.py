from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Library(db.Model):
    __tablename__ = 'Library'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'year': self.year}
    
with app.app_context():
    db.create_all()


@app.route('/library', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'Library test route'}), 200)


@app.route('/library', methods=['POST'])
def create_data_library():
    try:
        data = request.get_json()
        new_library = Library(title=data['title'], author=data['author'], year=data['year'])
        db.session.add(new_library)
        db.session.commit()
        return make_response(jsonify({'message': 'Library data created'}), 201)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to create data'}), 500)
    

@app.route('/library/<int:id>', methods=['GET'])
def get_data_library(id):
    try:
        library = Library.query.get(id)
        if library:
            return make_response(jsonify({'library_data': library.json()}), 200)
        return make_response(jsonify({'message': 'Library data not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get data'}), 500)


@app.route('/library/<int:id>', methods=['PUT'])
def update_data_library(id):
    try:
        library = Library.query.get(id)
        if library:
            data = request.get_json()
            library.title = data['title']
            library.author = data['author']
            library.year = data['year']
            db.session.commit()
            return make_response(jsonify({'message': 'Library data updated'}), 200)
        return make_response(jsonify({'message': 'Library data not found'}), 404)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to update data'}), 500)


@app.route('/library/<int:id>', methods=['DELETE'])
def delete_library_data(id):
    try:
        library = Library.query.get(id)
        if library:
            db.session.delete(library)
            db.session.commit()
            return make_response(jsonify({'message': 'Library data deleted'}), 200)
        return make_response(jsonify({'message': 'Library data not found'}), 404)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to delete data'}), 500)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Library API</h1>", 200


if __name__ == '__main__':
    app.run(debug=True)
