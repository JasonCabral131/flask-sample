from flask import jsonify, request
import numpy as np
from models import items, Item
import views
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from fuzzywuzzy import process

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower())
movies_data = pd.read_csv('./mockData/movies.csv')
ratings_data = pd.read_csv('./mockData/ratings.csv')
merged_data = pd.merge(ratings_data, movies_data, on='movieId')
movies_data['title_cleaned'] = movies_data['title'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x.lower()))

# Fit and transform the CountVectorizer on the cleaned movie titles
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), binary=False)
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_data['title_cleaned'])
average_ratings = merged_data.groupby('movieId')['rating'].mean().reset_index()

def collaborativeFilteringLatestAndHighestMovieRatings():
    try:
        query = request.args.get('query', '')

        if query:
            query_cleaned = clean_text(query)
            movies_data['similarity_score'] = movies_data['title_cleaned'].apply(lambda x: process.extractOne(query_cleaned, [x])[1])
            recommended_movies = movies_data.sort_values(by='similarity_score', ascending=False).head(10)
            recommended_movies.drop(columns=['similarity_score'], inplace=True)
            recommended_movies = pd.merge(recommended_movies, average_ratings, on='movieId')
            recommended_movies['rating'] = recommended_movies['rating'].round(1)
        else:
            top_10_movies = average_ratings.sort_values(by='rating', ascending=False).head(10)
            recommended_movies = pd.merge(top_10_movies, movies_data, on='movieId')
            recommended_movies['rating'] = recommended_movies['rating'].round(1)
        if recommended_movies.empty:
            return jsonify({'message': 'No matching movies found.'}), 404
        

        result = recommended_movies.to_dict(orient='records')
        return jsonify({"highest_ratings_movies": result}), 200
    except Exception as e:
        return jsonify({'message': 'error', 'info': str(e)}), 500

def recommendationView(): 
    return views.render_recommendationMovies()
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

