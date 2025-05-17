import pandas as pd
import pickle

# Full path to your movies.csv file
csv_path = "ml-latest-small/ml-latest-small/movies.csv"

# Load the CSV
df = pd.read_csv(csv_path)

# Use only the 'title' column and initialize a blank 'poster_url'
df = df[['title']].copy()
df['poster_url'] = ""

# Save as a pickle file for use in update_posters.py
with open("movies_meta.pkl", "wb") as f:
    pickle.dump(df, f)

print("✅ movies_meta.pkl created successfully.")
