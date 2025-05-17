import pandas as pd
import requests
import time
import pickle

API_KEY = "5db6b2b7"

def get_omdb_poster(title):
    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url)
        data = response.json()
        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return f"https://via.placeholder.com/300x450.png?text={title.replace(' ', '+')}"
    except Exception as e:
        print(f"Error fetching poster for '{title}':", e)
        return f"https://via.placeholder.com/300x450.png?text={title.replace(' ', '+')}"

# Load existing metadata
with open("movies_meta.pkl", "rb") as f:
    movies = pickle.load(f)

# Update poster URLs using OMDb API
movies['poster_url'] = movies['title'].apply(get_omdb_poster)

# Optional: Pause between API calls to respect rate limits
    # time.sleep(0.25)  # Uncomment if needed (4 requests/sec limit on free OMDb tier)

# Save updated metadata back
with open("movies_meta.pkl", "wb") as f:
    pickle.dump(movies, f)

print("✅ Poster update complete! Real posters are now saved in movies_meta.pkl.")
