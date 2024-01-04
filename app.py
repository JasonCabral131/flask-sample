from flask import Flask, jsonify, request

app = Flask(__name__)
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    found_item = None

    for item in items:
        if item['id'] == item_id:
            found_item = item
            break

    if found_item:
        return jsonify({'item': found_item}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = {'id': len(items) + 1, 'name': data['name']}
    items.append(new_item)
    return jsonify({'item': new_item}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        data = request.get_json()
        item['name'] = data['name']
        return jsonify({'item': item})
    return jsonify({'message': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(port=5000)