import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

def load_data(csv_path="../anime_data/anilist.csv", max_features=5000):
    try:
        data = pd.read_csv(csv_path)
        for col in ['title_english', 'title_romaji', 'description', 'genres', 'tags', 'image', 'episodes']:
            if col not in data.columns:
                data[col] = ''
            else:
                data[col] = data[col].astype(str).fillna('')

        # Combine features
        data['combined_features'] = (
            data['title_english'] + ' ' +
            data['genres'] + ' ' +
            data['tags'] + ' ' +
            data['description']
        ).apply(clean_text)

        # TF-IDF
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=max_features)
        ftr_mtrx = vectorizer.fit_transform(data['combined_features']).tocsr()

        print("✅ Data and TF-IDF matrix loaded successfully!")
        return data, ftr_mtrx, vectorizer

    except FileNotFoundError:
        print("❌ CSV file not found!")
        return None, None, None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None, None

# Usage: data, ftr_mtrx, vectorizer = load_data()
