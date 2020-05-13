from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

# dummy data
ratings = [
    {
        'movie': 'this is a movie title',
        'year': 'this is the year of the movie',
        'bio': 'this is a short biography',
        'rating': '5'
    },
    {
        'movie': 'this is another movie title',
        'year': 'this is another year of the movie',
        'bio': 'this is another short biography',
        'rating': '0'
    }
]

# routing to main page
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html', ratings=ratings)

# like button function
@app.route('/like', methods=['GET', 'POST'])
def like():
    print("5")
    return "5"

# dislike button function
@app.route('/dislike', methods=['GET', 'POST'])
def dislike():
    print("0")
    return "0"

# routing to results page
@app.route('/results')
def results():
    return render_template('results.html', title="Results")


if __name__ == '__main__':
    # if code is changed, the web app will automatically reload
    app.run(debug=True)
