from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Document/APIs/2nd List Api modles/1.Api/instance/database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name={self.name}, email={self.email})'

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name can't be blank")
user_args.add_argument('email', type=str, required=True, help="Email can't be blank")

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        return UserModel.query.all()
    
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        new_user = UserModel(name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return UserModel.query.all(), 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user
    
    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return user

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)