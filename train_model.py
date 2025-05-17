import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import numpy as np

# Load data
ratings = pd.read_csv(r"C:\Users\HP\OneDrive\Dokumen\movie\ml-latest-small\ml-latest-small\ratings.csv")
movies = pd.read_csv(r"C:\Users\HP\OneDrive\Dokumen\movie\ml-latest-small\ml-latest-small\movies.csv")

# Merge ratings and movies
data = pd.merge(ratings, movies, on='movieId')
user_item_matrix = data.pivot_table(index='userId', columns='title', values='rating').fillna(0)

# Cosine similarity
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

# Save models
os.makedirs('model', exist_ok=True)
with open('model/similarity.pkl', 'wb') as f:
    pickle.dump(item_similarity_df, f)
with open('model/user_ratings.pkl', 'wb') as f:
    pickle.dump(user_item_matrix, f)

print("✅ Model saved successfully.")

# ------------------ Performance Evaluation ------------------ #
def recommend_for_user(user_id, user_ratings, similarity):
    if user_id not in user_ratings.index:
        return []
    user_rated = user_ratings.loc[user_id]
    liked_movies = user_rated[user_rated >= 4].index.tolist()
    scores = pd.Series(dtype='float64')
    for movie in liked_movies:
        similar_scores = similarity[movie]
        scores = scores.add(similar_scores, fill_value=0)
    scores = scores.drop(liked_movies, errors='ignore')
    return scores.sort_values(ascending=False).head(10).index.tolist()

# Evaluation
precisions, recalls, f1s, accuracies = [], [], [], []
scatter_x, scatter_y = [], []

for user_id in user_item_matrix.index:
    user_data = user_item_matrix.loc[user_id]
    liked_movies = user_data[user_data >= 4]

    if len(liked_movies) < 5:
        continue

    test_movies = liked_movies.sample(n=2, random_state=42)
    train_movies = liked_movies.drop(test_movies.index)

    temp_matrix = user_item_matrix.copy()
    temp_matrix.loc[user_id, test_movies.index] = 0

    recommended = recommend_for_user(user_id, temp_matrix, item_similarity_df)
    predicted_set = set(recommended)
    actual_set = set(test_movies.index)

    true_positives = len(predicted_set & actual_set)
    precision = true_positives / len(predicted_set) if predicted_set else 0
    recall = true_positives / len(actual_set) if actual_set else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    accuracy = true_positives / 10  # since we get top 10 recommendations

    precisions.append(precision)
    recalls.append(recall)
    f1s.append(f1)
    accuracies.append(accuracy)
    scatter_x.append(precision)
    scatter_y.append(recall)

# ------------------ Print Metrics ------------------ #
print("\n📊 Performance Metrics:")
print(f"Average Precision : {np.mean(precisions):.3f}")
print(f"Average Recall    : {np.mean(recalls):.3f}")
print(f"Average F1-Score  : {np.mean(f1s):.3f}")
print(f"Average Accuracy  : {np.mean(accuracies):.3f}")

# ------------------ Visualizations ------------------ #
plt.figure(figsize=(12, 8))

# Bar Chart
plt.subplot(2, 2, 1)
metrics = ['Precision', 'Recall', 'F1 Score', 'Accuracy']
scores = [np.mean(precisions), np.mean(recalls), np.mean(f1s), np.mean(accuracies)]
colors = ['cornflowerblue', 'mediumseagreen', 'salmon', 'gold']
plt.bar(metrics, scores, color=colors)
plt.ylim(0, 1)
plt.title('Average Metrics')
plt.ylabel('Score')
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Scatter Plot
plt.subplot(2, 2, 2)
plt.scatter(scatter_x, scatter_y, alpha=0.6, color='purple')
plt.xlabel('Precision')
plt.ylabel('Recall')
plt.title('Precision vs Recall per User')
plt.grid(True)

# Heatmap (subset of similarity matrix)
plt.subplot(2, 1, 2)
subset = item_similarity_df.iloc[:10, :10]
sns.heatmap(subset, cmap='coolwarm', xticklabels=True, yticklabels=True)
plt.title('Item-Item Similarity (Top 10 Movies)')
plt.tight_layout()
plt.show()
