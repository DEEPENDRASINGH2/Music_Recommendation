from flask import Flask, render_template, request, jsonify
import pickle
import os
import requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)

# =========================
# LOAD MODEL
# =========================
df = pickle.load(open(os.path.join(BASE_DIR, 'model/df.pkl'), 'rb'))
model = pickle.load(open(os.path.join(BASE_DIR, 'model/model.pkl'), 'rb'))
tfidf = pickle.load(open(os.path.join(BASE_DIR, 'model/tfidf.pkl'), 'rb'))

df = df.fillna('')

df['song_lower'] = df['song'].str.lower()
df['artist_lower'] = df['artist'].str.lower()
df['text_lower'] = df['text'].str.lower()

cache = {}

# 🔑 ADD YOUR API KEY
YOUTUBE_API_KEY = "AIzaSyCj9hi8lX4fKKoWa4itv38cZ_H6nItfcHQ"


# =========================
# 🎬 YOUTUBE SEARCH
# =========================
def youtube_search(query, max_results=5):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": query + " song",
            "key": YOUTUBE_API_KEY,
            "maxResults": max_results,
            "type": "video"
        }

        res = requests.get(url, params=params).json()

        results = []

        for item in res.get("items", []):
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
            video_id = item["id"]["videoId"]

            results.append({
                "song": title,
                "artist": channel,
                "image": thumbnail,
                "youtube": f"https://www.youtube.com/watch?v={video_id}",
                "embed": f"https://www.youtube.com/embed/{video_id}"
            })

        return results

    except:
        return []


# =========================
# 🔥 TRENDING
# =========================
def get_trending():
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"

        params = {
            "part": "snippet",
            "chart": "mostPopular",
            "regionCode": "IN",
            "videoCategoryId": "10",  # music
            "maxResults": 5,
            "key": YOUTUBE_API_KEY
        }

        res = requests.get(url, params=params).json()

        results = []

        for item in res.get("items", []):
            video_id = item["id"]

            results.append({
                "song": item["snippet"]["title"],
                "artist": item["snippet"]["channelTitle"],
                "image": item["snippet"]["thumbnails"]["high"]["url"],
                "youtube": f"https://www.youtube.com/watch?v={video_id}",
                "embed": f"https://www.youtube.com/embed/{video_id}"
            })

        return results

    except:
        return []


# =========================
# 🤖 AI + YOUTUBE HYBRID
# =========================
def recommend(query):

    if not query:
        return []

    query = query.lower()

    if query in cache:
        return cache[query]

    try:
        # 🔍 Dataset match
        mask = (
            df['song_lower'].str.contains(query, na=False, regex=False) |
            df['artist_lower'].str.contains(query, na=False, regex=False)
        )

        matches = df[mask]

        # =========================
        # 🎯 AI MODEL PART
        # =========================
        if not matches.empty:

            idx = matches.index[0]

            text_data = (
                df.iloc[idx]['song'] + " " +
                df.iloc[idx]['artist'] + " " +
                df.iloc[idx]['text']
            )

            query_vec = tfidf.transform([text_data])
            _, indices = model.kneighbors(query_vec, n_neighbors=3)

            ai_songs = [
                df.iloc[i]['song'] for i in indices[0]
            ]

            # 🔥 combine with YouTube
            yt_results = youtube_search(ai_songs[0], 5)

        else:
            # 🌍 direct YouTube
            yt_results = youtube_search(query, 5)

        cache[query] = yt_results
        return yt_results

    except Exception as e:
        return [{"song": "Error", "artist": str(e)}]


# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    trending = get_trending()
    return render_template('index.html', trending=trending)


@app.route('/recommend', methods=['POST'])
def get_recommendation():
    song = request.form.get('song')
    results = recommend(song)
    trending = get_trending()
    return render_template('index.html', songs=results, trending=trending)


@app.route('/suggest')
def suggest():
    query = request.args.get('q', '').lower()

    if not query:
        return jsonify([])

    suggestions = df[
        df['song_lower'].str.contains(query, na=False, regex=False)
    ]['song'].head(5).tolist()

    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)