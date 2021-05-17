import pandas as pd
import numpy as np
import pickle
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


ratings = pd.read_csv('./data/ratings.csv',
                      usecols=['userId', 'movieId', 'rating'],
                      dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'}
                     )

movies = pd.read_csv('./data/movies.csv',
                     usecols=['movieId', 'title'],
                     dtype={'movieId': 'int32', 'title': 'str'}
                    )

df = pd.merge(ratings, movies, on='movieId')

ratings_count = df.groupby('title', as_index=False)['rating'].count().rename(
                columns = {'rating': 'ratingsCount'})

movies = pd.merge(movies, ratings_count, on='title')

average_rating = df.groupby('title', as_index=False)['rating'].mean().rename(
                 columns = {'rating': 'averageRating'})
movies = pd.merge(movies, average_rating, on='title')

df = df.merge(ratings_count, how='left', left_on='title', right_on='title')

popular_threshold = 20
popular_movies = df.query('ratingsCount > @popular_threshold')

movie_features = popular_movies.pivot_table(index='title',
                                            columns='userId',
                                            values='rating').fillna(0)
pickle.dump(movie_features, open("movie_features.pkl", "wb"))

movie_matrix = csr_matrix(movie_features)
pickle.dump(movie_matrix, open("movie_matrix.pkl", "wb"))

model = NearestNeighbors(algorithm='brute', metric='cosine')
model.fit(movie_matrix)

pickle.dump(model, open('model.pkl', 'wb'))

def movieRecommender(movie_name):
    movie_row = movie_features[movie_features.index.str.contains(movie_name)]
    query_index = np.random.choice(movie_features.shape[0])
    print(f"Index to search: {query_index}")
    _, indices = model.kneighbors(movie_row,
                                        n_neighbors=11)
    for i in range(len(indices.flatten())):
        if i == 0:
            print(f"Recommendations for {movie_features.index[indices.flatten()[i]]}:\n")
        else:
            print(f"{i}: {movie_features.index[indices.flatten()[i]]}")
