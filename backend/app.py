from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a Todo model.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

# Create the tables (run this once or use migrations)
with app.app_context():
    db.create_all()

# Endpoint to list all todos.
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    # Serialize list of todos
    todos_list = [{'id': t.id, 'task': t.task} for t in todos]
    return jsonify({'todos': todos_list}), 200

# Endpoint to create a new todo.
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    # Basic validation to ensure 'task' is present.
    if not data or 'task' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Task is required'}), 400

    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created', 'id': new_todo.id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
