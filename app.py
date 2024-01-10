from flask import Flask
from flask_cors import CORS
import controllers

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return controllers.index()

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    return controllers.get_item(item_id)

@app.route('/add_item', methods=['GET'])
def add_item_page():
    return controllers.add_item_page()

@app.route('/api/add_item', methods=['POST'])
def add_item():
    return controllers.add_item()

@app.route('/update_item/<int:item_id>', methods=['GET'])
def update_item_page(item_id):
    return controllers.update_item_page(item_id)

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    return controllers.update_item(item_id)

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return controllers.delete_item(item_id)

@app.route("/api/recommendations", methods=['GET'])
def get_recommendations():
     return controllers.collaborativeFilteringLatestAndHighestMovieRatings()

@app.route("/recommendations", methods=['GET'])
def recommendations():
     return controllers.recommendationView()

if __name__ == '__main__':
    app.run(debug=True)
