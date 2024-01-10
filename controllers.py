from flask import jsonify, request
from models import items, Item
import views

def index():
    return views.render_items(items)

def get_item(item_id):
    found_item = next((item for item in items if item.id == item_id), None)

    if found_item:
        return views.render_item(found_item)
    else:
        return jsonify({'message': 'Item not found'}), 404

def add_item_page():
    return views.render_add_item_page()

def add_item():
    data = request.get_json()
    new_item = Item(len(items) + 1, data['name'])
    items.append(new_item)
    return jsonify({'item': {'id': new_item.id, 'name': new_item.name}}), 201

def update_item_page(item_id):
    item = next((item for item in items if item.id == item_id), None)

    if item:
        return views.render_update_item_page(item)
    else:
        return jsonify({'message': 'Item not found'}), 404

def update_item(item_id):
    item = next((item for item in items if item.id == item_id), None)
    if item:
        data = request.get_json()
        item.name = data['name']
        return jsonify({'item': {'id': item.id, 'name': item.name}})
    return jsonify({'message': 'Item not found'}), 404

def delete_item(item_id):
    global items
    items = [item for item in items if item.id != item_id]
    return jsonify({'message': 'Item deleted'})
