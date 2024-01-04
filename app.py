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

if __name__ == '__main__':
    app.run(port=5000)