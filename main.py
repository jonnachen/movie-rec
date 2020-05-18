# imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import urllib.request as u_request
import ssl
import random

# instance of flask class
app = Flask(__name__)

# api information
api_key = "3dbf9b55bdf367747f40974789edbff7"
base_url = "https://api.themoviedb.org/3/discover/movie/?api_key="+api_key

# routing

# routing to main page


@app.route('/', methods=['GET', 'POST'])
def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    conn = u_request.urlopen(base_url)
    json_data = json.loads(conn.read())
    return render_template('index.html', movie=random.choice(json_data["results"]))

# like button function
@app.route('/like', methods=['GET', 'POST'])
def like():
    print("5")
    return "5"

# unknown button function
@app.route('/unknown', methods=['GET', 'POST'])
def unknown():
    #rated_movie = request.form.get('rating')
    # print(rated_movie)
    print("0")
    return "0"

# dislike button function
@app.route('/dislike', methods=['GET', 'POST'])
def dislike():
    print("-5")
    return "-5"

# routing to results page
@app.route('/results')
def results():
    return render_template('results.html', title="Results")


if __name__ == '__main__':
    # if code is changed, the web app will automatically reload
    app.run(debug=True)
