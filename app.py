from flask import Flask, jsonify, render_template ,request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
items = [
    {"id": 1, "name": "Gomez"},
    {"id": 2, "name": "Burgoz"},
    {"id": 3, "name": "Zamora"},
]

@app.route('/')
def index():
    return render_template('items_list.html', items=items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    found_item = None

    for item in items:
        if item['id'] == item_id:
            found_item = item
            break

    if found_item:
      return render_template('items_list.html', items=[found_item])
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/add_item', methods=['GET'])
def add_item_page():
    return render_template('add_item.html')

@app.route('/api/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = {'id': len(items) + 1, 'name': data['name']}
    items.append(new_item)
    print(items)
    return jsonify({'item': new_item}), 201

@app.route('/update_item/<int:item_id>', methods=['GET'])
def update_item_page(item_id):
    item = next((item for item in items if item['id'] == item_id), None)

    if item:
        return render_template('update_item.html', item=item)
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    print(item_id)
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
    app.run(debug=True)