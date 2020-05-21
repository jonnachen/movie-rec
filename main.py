# imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import urllib.request as u_request
import random
import urllib.parse
import requests
from movie import Movie
from recommender import Recommender

# instance of flask class
app = Flask(__name__)

# TMDB API
api_key = "3dbf9b55bdf367747f40974789edbff7"
base_url = "https://api.themoviedb.org/3"

discover = "/discover/movie/?api_key=" + \
    api_key+"&sort_by=popularity.desc&page="

# entire list of movie objects
movie_lib = []

# return api_url


def api_url(page_num):
    return base_url+discover+str(page_num)


# iterate through pages and add movies to movie_lib
for page in range(1, 11):
    url = api_url(page)

    # get data using API
    response = requests.get(url)

    # convert data to dictionary
    dictionary = json.loads(response.text)

    # get list of dictionaries of movies
    discover_movies = dictionary["results"]

    # store all dictionaries as movies in movie_lib
    for movie_dict in discover_movies:
        movie_lib.append(Movie(movie_dict))

# store rated movies here in the form [[rated_movie, rating]]
# example: [[<movie.Movie object at 0x10d76e110>, 'like'],
# [<movie.Movie object at 0x10e671f10>, 'dislike'],
# [<movie.Movie object at 0x10e661150>, 'like'],
# [<movie.Movie object at 0x10e66c6d0>, 'dislike'],
# [<movie.Movie object at 0x10e5f5110>, 'like'],
# [<movie.Movie object at 0x10e66c2d0>, 'dislike'],
# [<movie.Movie object at 0x10e65bb10>, 'like'],
# [<movie.Movie object at 0x10e5e15d0>, 'dislike'],
# [<movie.Movie object at 0x10e61e650>, 'like'],
# [<movie.Movie object at 0x10e61e590>, 'dislike']]
personal_ratings = []

# list of all movies rated
# example: [<movie.Movie object at 0x10551c190>,
# <movie.Movie object at 0x105578950>,
# <movie.Movie object at 0x105578990>,
# <movie.Movie object at 0x105588490>,
# <movie.Movie object at 0x1055939d0>,
# <movie.Movie object at 0x105591d50>,
# <movie.Movie object at 0x1055787d0>,
# <movie.Movie object at 0x1055b5450>,
# <movie.Movie object at 0x1055b1e90>,
# <movie.Movie object at 0x1055a57d0>]
rated_history = []
# TO-DO: empty this list each time app is restarted?

# number of movies rated so far
num_rated = 0

# return a movie that has not yet been rated


def choose_unique_film():
    unique = False
    while (not unique):
        exists = False
        random_movie = random.choice(movie_lib)
        for rated in rated_history:
            if random_movie == rated:
                exists = True
        if exists == False:
            unique = True

    return random_movie

# iterates through rated_history and returns movie object


def get_movie(id):
    for movie in rated_history:
        if movie.id == int(id):
            return movie


def check_ten(personal_ratings, num_rated):
    print(num_rated)
    return (num_rated >= 10)


def check_personal_ratings(personal_ratings):
    not (personal_ratings == [])


def check_tour(num_rated):
    print(num_rated)
    return (num_rated > 1)

# routing

# routing to main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/#', methods=['GET', 'POST'])
def main():
    has_started_rating = bool(request.form.get('has_started_rating'))

    if request.method == 'POST'and has_started_rating:
        # movie was rated via form

        global num_rated
        # gather data from form
        rated_movie_id = request.form.get('movie_id_rated')
        rating = request.form.get('rating')

        if rating == 'unknown':
            num_rated -= 1
        elif rating == 'like':
            personal_ratings.append([get_movie(rated_movie_id), rating])

        num_rated += 1

    if check_ten(personal_ratings, num_rated):
        return redirect(url_for('results'))

    # get a random + unique movie from movie list
    random_movie = choose_unique_film()

    # add to the history of movies that have been shown so far
    rated_history.append(random_movie)

    return render_template('index.html', movie=random_movie, tour=check_tour(num_rated))

# routing to results page
@app.route('/results')
def results():
    # if personal_rating list is empty, reroute to 404 page
    if check_personal_ratings(personal_ratings):
        return redirect(url_for('to404'))

    try:
        # below is currently for front-end purposes
        # result = choose_unique_film()
        # percent_match = "86%"

        recommender = Recommender(personal_ratings)
        result = recommender.get_result()
        release_year = result.release_date[0:4]
        percent_match = "it's a match!"
        return render_template('results.html', title="Results", result=result, release_year=release_year, percent_match=percent_match)

    except Exception as e:
        return redirect(url_for('to404'))


# 404 error page
@app.errorhandler(404)
def error(e):
    return redirect(url_for('to404'))


@app.route('/404')
def to404():
    return render_template('404.html', title="404 error")


if __name__ == '__main__':
    # if code is changed, the web app will automatically reload
    app.run(debug=True)
