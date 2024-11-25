from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL') or 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def json(self):
        return {'id': self.id, 'task': self.task, 'completed': self.completed}

with app.app_context():
    db.create_all()

@app.route('/todos', methods=['GET'])
def get_todos():
    try:
        todos = Todo.query.all()
        return make_response(jsonify({'todos': [todo.json() for todo in todos]}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get todos'}), 500)

@app.route('/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        if not data.get('task'): 
            return make_response(jsonify({'message': 'Task is required'}), 400)
        new_todo = Todo(task=data['task'], completed=data.get('completed', False))
        db.session.add(new_todo)
        db.session.commit()
        return make_response(jsonify({'message': 'Todo created successfully'}), 201)
    except SQLAlchemyError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to create todo'}), 500)

@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    try:
        todo = Todo.query.get(id)
        if todo:
            return make_response(jsonify({'todo': todo.json()}), 200)
        return make_response(jsonify({'message': 'Todo not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Failed to get todo'}), 500)

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    try:
        todo = Todo.query.get(id)
        if todo:
            data = request.get_json()
            todo.task = data['task']
            todo.completed = data['completed']
            db.session.commit()
            return make_response(jsonify({'message': 'Todo updated successfully'}), 200)
        return make_response(jsonify({'message': 'Todo not found'}), 404)
    except SQLAlchemyError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to update todo'}), 500)

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        todo = Todo.query.get(id)
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return make_response(jsonify({'message': 'Todo deleted successfully'}), 200)
        return make_response(jsonify({'message': 'Todo not found'}), 404)
    except SQLAlchemyError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Failed to delete todo'}), 500)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Todo List API</h1>", 200

if __name__ == '__main__':
    app.run(debug=True)