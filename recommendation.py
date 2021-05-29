import pickle
import numpy as np
from fuzzywuzzy import process

model = pickle.load(open("model.pkl", "rb"))
movie_features = pickle.load(open("movie_features.pkl", "rb"))

def movieSearch(query):
    result = process.extract(query, movie_features.index.tolist())
    matches = [x[0] for x in result]
    return matches


def movieRecommender(movie_name):
    movie = process.extractOne(movie_name, movie_features.index)[0]
    movie_row = movie_features[movie_features.index == movie]
    query_index = np.random.choice(movie_features.shape[0])
    print(f"Index to search: {query_index}")
    recommendations = []
    if movie_row.empty:
        return 0, 1
    _, indices = model.kneighbors(movie_row,
                                        n_neighbors=9)
    
    movie = movie_features.index[indices.flatten()[0]]
    for i in range(1, 9):
        recommendations.append(movie_features.index[indices.flatten()[i]])
        
    return movie, recommendations
