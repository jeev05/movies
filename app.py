from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load similarity matrix and user ratings
with open('model/similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

with open('model/user_ratings.pkl', 'rb') as f:
    user_ratings = pickle.load(f)

@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        user_id = int(request.args.get('user_id'))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user_id"}), 400

    if user_id not in user_ratings.index:
        return jsonify([])

    user_rated = user_ratings.loc[user_id]
    liked_movies = user_rated[user_rated >= 4].index.tolist()

    scores = pd.Series(dtype='float64')
    for movie in liked_movies:
        similar_scores = similarity[movie]
        scores = scores.add(similar_scores, fill_value=0)

    scores = scores.drop(liked_movies, errors='ignore')
    top_recommendations = scores.sort_values(ascending=False).head(10)
    results = [{'title': title, 'score': round(score, 2)} for title, score in top_recommendations.items()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
