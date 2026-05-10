from flask import Flask, request, jsonify
from flask_cors import CORS
from data_loader import load_data
from recommender import make_cached_recommend

app = Flask(__name__)
CORS(app)

# Load data
data, ftr_mtrx, vectorizer = load_data()
cached_recommend = make_cached_recommend(data, ftr_mtrx)

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    if data is None or ftr_mtrx is None:
        return jsonify({'error': 'Backend not ready.'}), 503

    req_data = request.get_json()
    if not req_data or 'animeTitle' not in req_data:
        return jsonify({'error': 'Missing "animeTitle"'}), 400

    anime_title = req_data['animeTitle']
    result = cached_recommend(anime_title)

    if not result['recommendations'] and not result['input_anime']:
        return jsonify({'error': f'Anime "{anime_title}" not found.'}), 404

    return jsonify(result)

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    cached_recommend.cache_clear()
    return jsonify({'message': 'Cache cleared ✅'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
