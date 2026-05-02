import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# =========================
# LOAD DATA (FIXED PATH)
# =========================
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, '', 'data', 'songdata.csv')

df = pd.read_csv(file_path)

# =========================
# PREPROCESS
# =========================
df = df[['artist', 'song', 'text']].dropna()

# =========================
# TF-IDF
# =========================
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['text'])

# =========================
# MODEL (NO MEMORY CRASH)
# =========================
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(tfidf_matrix)

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(song_name):
    if song_name not in df['song'].values:
        return ["Song not found"]

    idx = df[df['song'] == song_name].index[0]

    distances, indices = nn.kneighbors(tfidf_matrix[idx], n_neighbors=6)

    recommendations = []
    for i in indices[0][1:]:
        recommendations.append(df.iloc[i].song)

    return recommendations

# =========================
# SAVE FILES
# =========================
pickle.dump(df, open('model/df.pkl', 'wb'))
pickle.dump(nn, open('model/model.pkl', 'wb'))
pickle.dump(tfidf, open('model/tfidf.pkl', 'wb'))

# =========================
# TEST RUN (TERMINAL)
# =========================
if __name__ == "__main__":
    print("Model running...\n")

    song = input("Enter song name: ")

    results = recommend(song)

    print("\nRecommended Songs:")
    for r in results:
        print(r)