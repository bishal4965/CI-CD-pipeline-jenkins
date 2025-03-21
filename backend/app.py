from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from prometheus_client import Counter, Histogram, generate_latest
import time
from urllib.parse import quote_plus
from sqlalchemy import inspect

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['method', 'endpoint'])

app = Flask(__name__)

# Get database configuration from environment
db_user = os.getenv('DB_USER', 'user')
db_password = quote_plus(os.getenv('DB_PASSWORD', 'user@1234'))
db_host = os.getenv('DB_HOST', 'db')
db_name = os.getenv('DB_NAME', 'appdb')

# Configure MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a Todo model with completed status
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # New field for completed status

# Create the tables
with app.app_context():
    # Check if table exists before creating
    inspector = inspect(db.engine)
    if not inspector.has_table('todo'):
        db.create_all()
    else:
        # Check if completed column exists, if not add it
        columns = [c['name'] for c in inspector.get_columns('todo')]
        if 'completed' not in columns:
            with db.engine.connect() as connection:
                connection.execute('ALTER TABLE todo ADD COLUMN completed BOOLEAN DEFAULT FALSE')


# Middleware for metrics
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path).inc()
    REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
    return response

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

# Prometheus metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()

# Endpoint to list all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = [{'id': t.id, 'task': t.task, 'completed': t.completed} for t in todos]
    return jsonify({'todos': todos_list}), 200

# Endpoint to create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Task is required'}), 400

    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created', 'id': new_todo.id}), 201

# Endpoint to delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Not Found', 'message': 'Todo not found'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200

# Endpoint to toggle todo completion status
@app.route('/todos/<int:todo_id>/toggle', methods=['PUT'])
def toggle_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Not Found', 'message': 'Todo not found'}), 404
    
    todo.completed = not todo.completed
    db.session.commit()
    return jsonify({'message': 'Todo updated', 'completed': todo.completed}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
