from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from recommendation import movieRecommender, movieSearch
from db import get_movies

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommendation.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    genres = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return "Movie names and genres database."
    
    
class Rating(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['POST', 'GET'])
def home():
    top_movies, popular_movies = get_movies()
    return render_template('index.html', top_movies=top_movies, popular_movies=popular_movies)

@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        query = request.form['q']
        matches = movieSearch(query)
        if type(matches) == int:
            return render_template('error.html')
        else:
            return render_template('results.html', query=query, matches=matches)
    else:
        return redirect(url_for('home'))

@app.route('/recommendation/<movie>', methods=['POST', 'GET'])
def recommendation(movie):
    movie_name = movie
    movie, recommendations = movieRecommender(movie_name)
    if type(recommendations) == int:
        return render_template('error.html')
    else:
        return render_template('recommendation.html', movie=movie, recommendations=recommendations)
