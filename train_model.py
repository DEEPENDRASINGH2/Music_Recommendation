import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('data/songdata.csv')
df = df.dropna()

df['tags'] = df['song'] + " " + df['artist'] + " " + df['text']

tfidf = TfidfVectorizer(max_features=3000, stop_words='english')

# 🔥 NO .toarray()
X = tfidf.fit_transform(df['tags'])

model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(X)

pickle.dump(df, open('model/df.pkl', 'wb'))
pickle.dump(model, open('model/model.pkl', 'wb'))
pickle.dump(tfidf, open('model/tfidf.pkl', 'wb'))

print("✅ Model trained (memory optimized)")