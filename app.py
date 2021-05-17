from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from recommendation import movieRecommender

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def home():
    
    return render_template('index.html')


@app.route('/recommendation/', methods=['POST', 'GET'])
def recommendation():
    if request.method == 'POST':
        movie_name = request.form['q']
        movie, recommendations = movieRecommender(movie_name)
        if type(recommendations) == int:
            return render_template('error.html')
        else:
            return render_template('recommendation.html', movie=movie, recommendations=recommendations)
    else:
        return redirect(url_for('home'))
