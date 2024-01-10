from flask import render_template, jsonify

def render_items(items):
    return render_template('items_list.html', items=items)

def render_item(item):
    return render_template('items_list.html', items=[item])

def render_add_item_page():
    return render_template('add_item.html')

def render_update_item_page(item):
    return render_template('update_item.html', item=item)
