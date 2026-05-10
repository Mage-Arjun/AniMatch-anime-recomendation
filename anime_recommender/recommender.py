from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache

def find_best_match(title, df):
    lower_title = title.lower()
    matches = df[df['title_english'].str.lower() == lower_title]
    if not matches.empty:
        return matches.index[0]

    partial_matches = df[df['title_english'].str.lower().str.contains(lower_title)]
    if not partial_matches.empty:
        return partial_matches.index[0]

    closest = get_close_matches(title, df['title_english'].tolist(), n=1, cutoff=0.6)
    if closest:
        return df[df['title_english'] == closest[0]].index[0]

    return None

def recommend(title, df, ftr_mtrx, top_n=10):
    if df is None or ftr_mtrx is None:
        return {'recommendations': [], 'input_anime': None}

    idx = find_best_match(title, df)
    if idx is None:
        return {'recommendations': [], 'input_anime': None}

    query_vec = ftr_mtrx[idx]
    sim_scores = cosine_similarity(query_vec, ftr_mtrx).flatten()

    input_anime_data = df.iloc[idx][['title_english', 'image', 'genres', 'tags', 'episodes']].to_dict()
    found_title = df.iloc[idx]['title_english']
    found_lower = found_title.lower()

    sim_scores = [
        score + 0.05 if found_lower in df.iloc[i]['title_english'].lower() and i != idx else score
        for i, score in enumerate(sim_scores)
    ]

    sim_indices = sorted(range(len(sim_scores)), key=lambda i: sim_scores[i], reverse=True)
    sim_indices = [i for i in sim_indices if i != idx][:top_n]

    recommendations_df = df.iloc[sim_indices][['title_english', 'image', 'genres', 'tags', 'episodes']].copy()
    recommendations_df['content_similarity'] = [sim_scores[i] for i in sim_indices]
    recommendations_df['title_is_similar'] = recommendations_df['title_english'].str.lower().apply(
        lambda x: 1 if found_lower in x and x != found_lower else 0
    )

    recommendations_df = recommendations_df.sort_values(
        by=['title_is_similar', 'content_similarity'], ascending=[True, False]
    )

    return {
        'recommendations': recommendations_df.to_dict('records'),
        'input_anime': input_anime_data
    }

# Cached version for Flask
def make_cached_recommend(df, ftr_mtrx):
    @lru_cache(maxsize=128)
    def cached(title):
        return recommend(title, df, ftr_mtrx)
    return cached
