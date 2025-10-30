import pandas as pd
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import re
import random

app = Flask(__name__)
CORS(app)

# --- 1. Load Data and Initialize Model ---
def clean_text(text):
    """Lowercase and remove special characters for better TF-IDF matching."""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

try:
    data = pd.read_csv("anime_data/anilist.csv")
    print("📊 Data loaded successfully!")
    # Ensure all relevant columns exist and are strings
    for col in ['title_english', 'title_romaji', 'description', 'genres', 'tags', 'image', 'episodes']:
        if col not in data.columns:
            data[col] = ''
        else:
            data[col] = data[col].astype(str).fillna('')
    
    # Combine features for TF-IDF
    data['combined_features'] = (
        data['title_english'] + ' ' +
        data['genres'] + ' ' +
        data['tags'] + ' ' +
        data['description']
    ).apply(clean_text)
    
    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english', max_features=5000)
    ftr_mtrx = vectorizer.fit_transform(data['combined_features'])
    
    # Cosine similarity matrix
    cosine_sim = cosine_similarity(ftr_mtrx, ftr_mtrx)
    
    print("✅ Model components loaded and initialized successfully!")

except FileNotFoundError:
    print("❌ Error: CSV file not found.")
    data = None
    cosine_sim = None
except Exception as e:
    print(f"❌ Error during initialization: {e}")
    data = None
    cosine_sim = None

# --- 2. Recommendation Logic ---
def find_best_match(title, df):
    """Find best index for input title (exact, partial, or fuzzy)."""
    lower_title = title.lower()
    
    # Exact match
    matches = df[df['title_english'].str.lower() == lower_title]
    if not matches.empty:
        return matches.index[0]
    
    # Partial match
    partial_matches = df[df['title_english'].str.lower().str.contains(lower_title)]
    if not partial_matches.empty:
        return partial_matches.index[0]
    
    # Fuzzy match
    closest = get_close_matches(title, df['title_english'].tolist(), n=1, cutoff=0.6)
    if closest:
        return df[df['title_english'] == closest[0]].index[0]
    
    return None

def recommend(title, df, cosim, top_n=10):
    if df is None or cosim is None:
        return {'recommendations': [], 'input_anime': None}
    
    idx = find_best_match(title, df)
    if idx is None:
        return {'recommendations': [], 'input_anime': None}
    
    input_anime_data = df.iloc[idx][['title_english', 'image', 'genres', 'tags', 'episodes']].to_dict()
    found_title = df.iloc[idx]['title_english']
    found_lower = found_title.lower()
    
    # Compute similarity and boost sequels/franchise matches slightly
    sim_scores = list(enumerate(cosim[idx]))
    sim_scores = [
        (i, score + 0.05 if found_lower in df.iloc[i]['title_english'].lower() and i != idx else score)
        for i, score in sim_scores
    ]
    
    # Sort by similarity descending, exclude input anime
    sim_scores = [s for s in sorted(sim_scores, key=lambda x: x[1], reverse=True) if s[0] != idx][:top_n]
    
    # Fallback: if no similarity, pick random anime
    if len(sim_scores) < top_n:
        remaining = set(df.index) - set([idx] + [i[0] for i in sim_scores])
        fallback = random.sample(list(remaining), top_n - len(sim_scores))
        sim_scores.extend([(i, 0) for i in fallback])
    
    # Build recommendations dataframe
    anime_indices = [i[0] for i in sim_scores]
    recommendations_df = df.iloc[anime_indices][['title_english', 'image', 'genres', 'tags', 'episodes']].copy()
    recommendations_df['content_similarity'] = [i[1] for i in sim_scores]
    recommendations_df['title_is_similar'] = recommendations_df['title_english'].str.lower().apply(
        lambda x: 1 if found_lower in x and x != found_lower else 0
    )
    
    # Sort: first avoid similar titles, then highest similarity
    recommendations_df = recommendations_df.sort_values(by=['title_is_similar', 'content_similarity'], ascending=[True, False])
    
    return {
        'recommendations': recommendations_df.to_dict('records'),
        'input_anime': input_anime_data
    }
    

# --- 3. API Endpoint ---
@app.route('/recommend', methods=['POST'])
def get_recommendation():
    if data is None or cosine_sim is None:
        return jsonify({'error': 'Backend not ready. Missing data or model components.'}), 503
    
    try:
        req_data = request.get_json()
        if not req_data or 'animeTitle' not in req_data:
            return jsonify({'error': 'Invalid request. Missing "animeTitle".'}), 400
        
        anime_title = req_data['animeTitle']
        result = recommend(anime_title, data, cosine_sim)
        
        if not result['recommendations'] and not result['input_anime']:
            return jsonify({'error': f'Anime title or keyword "{anime_title}" not found.'}), 404
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

# --- 4. Run Server ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
