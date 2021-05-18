import pickle
import numpy as np

model = pickle.load(open("model.pkl", "rb"))
movie_features = pickle.load(open("movie_features.pkl", "rb"))

def movieRecommender(movie_name):
    movie_row = movie_features[movie_features.index.str.contains(movie_name)]
    query_index = np.random.choice(movie_features.shape[0])
    print(f"Index to search: {query_index}")
    recommendations = []
    if movie_row.empty:
        return 0, 1
    _, indices = model.kneighbors(movie_row,
                                        n_neighbors=11)
    
    movie = movie_features.index[indices.flatten()[0]]
    for i in range(1, 9):
        recommendations.append(movie_features.index[indices.flatten()[i]])
        
    return movie, recommendations
