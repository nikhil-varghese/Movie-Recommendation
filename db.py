import pandas as pd
import sqlite3


def get_movies():
    conn = sqlite3.connect("movielens.db")

    # movies = pd.read_csv("./data/movies.csv")
    # print(movies.head())

    # ratings = pd.read_csv("./data/ratings.csv")
    # print(ratings.head())

    # links = pd.read_csv("./data/links.csv")
    # print(links.head())

    # tags = pd.read_csv("./data/tags.csv")
    # print(tags.head())

    # movies.to_sql('movies', conn, if_exists="replace", index=False)

    # ratings.to_sql('ratings', conn, if_exists="replace", index=False)

    # links.to_sql('links', conn, if_exists="replace", index=False)

    # tags.to_sql('tags', conn, if_exists="replace", index=False)

    cur = conn.cursor()
    
    top_movies = []
    for row in cur.execute("SELECT m.title, ROUND(SUM(r.rating)/COUNT(r.rating), 2) as avg_rating, COUNT(r.rating) FROM movies as m \
                        JOIN ratings as r ON m.movieId=r.movieId \
                        GROUP BY r.movieId \
                        HAVING COUNT(r.rating) > 100 \
                        ORDER BY avg_rating DESC \
                        LIMIT 8"):
        top_movies.append(row)
        
    popular_movies = []
    for row in cur.execute("SELECT m.title, ROUND(SUM(r.rating)/COUNT(r.rating), 2) as avg_rating, COUNT(r.rating) FROM movies as m \
                        JOIN ratings as r ON m.movieId=r.movieId \
                        GROUP BY r.movieId \
                        ORDER BY COUNT(r.rating) DESC \
                        LIMIT 8"):
        popular_movies.append(row)
        
        
    print(f"TOP movies: {top_movies}")
    print(f"Popular movies: {popular_movies}")
    
    return top_movies, popular_movies