# imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import urllib.request as u_request
import random
import urllib.parse
import requests
from movie import Movie

# instance of flask class
app = Flask(__name__)

# TMDB API
api_key = "3dbf9b55bdf367747f40974789edbff7"
base_url = "https://api.themoviedb.org/3"

discover = "/discover/movie/?api_key="+api_key

# get data using API
response = requests.get(base_url+discover)

# convert data to dictionary
dictionary = json.loads(response.text)

# get dictionary of movies
discover_movies = dictionary["results"]

# store rated movies here in the form [[rated_movie, rating]]
# for testing reasons, for now, only store movie name
personal_ratings = []

# all movies rated
rated_history = []
# TO-DO: empty this list each time app is restarted?

# TO-DO: fix unique film function


def choose_unique_film():
    unique = False
    random_movie = None
    while (not unique):
        exists = False
        random_movie = Movie(random.choice(discover_movies))
        for rated in rated_history:
            if random_movie == rated:
                exists = True
        if exists == False:
            unique = True
    return random_movie


# routing

# routing to main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/#', methods=['GET', 'POST'])
def main():
    # TO-DO: fix GET 404 error
    if request.method == 'POST':
        # movie was rated via form

        rated_movie_id = request.form.get('movie_rated')

        # get movie data using API
        response = requests.get(
            base_url+"/movie/"+rated_movie_id+"?api_key="+api_key+"&language=en-US")

        # convert data to dictionary - rated movie in dictonary form
        rated_movie = json.loads(response.text)

        print(rated_movie)
        rating = request.form.get('rating')

        personal_ratings.append([rated_movie["title"], rating])
        print("personal ratings:")
        print(personal_ratings)

    # get a random movie from the dict
    random_movie = choose_unique_film()

    rated_history.append(random_movie)
    print("history rated")
    print(rated_history)

    return render_template('index.html', movie=random_movie)

# routing to results page
@app.route('/results')
def results():
    return render_template('results.html', title="Results")


if __name__ == '__main__':
    # if code is changed, the web app will automatically reload
    app.run(debug=True)
