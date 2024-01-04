from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage (replace this with a database in production)
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]

# Routes
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

