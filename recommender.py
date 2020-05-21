import requests
import json
from movie import Movie


class Recommender:
    def __init__(self, result_list):
        self.result_list = result_list

    # takes in a result_list and returns a list that only contains the 'liked' movies
    def get_liked(self, result_list):
        liked = []
        for pair in result_list:
            if pair[1] == 'like':
                liked.append(pair[0])
        return liked

    # takes in a Movie object and returns a list of recommended Movie objects
    def get_recommended(self, movie):
        movie_id = movie.id

        recommended = []

        for page in range(1, 11):
            # get data using API
            response = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) +
                                    "/recommendations?api_key=3dbf9b55bdf367747f40974789edbff7&language=en-US&page=" + str(page))

            # convert data to dictionary
            dictionary = json.loads(response.text)

            # get list of dictionaries of movies
            rec_movies = dictionary["results"]

            for movie in rec_movies:
                recommended.append(Movie(movie))

        return recommended

    def get_result(self):
        # for each 'liked' movie, create lists of recommended movies
        # iterate through each list and add it to a hashmap/dictionary
        # where the key is the movie id and the value is the number of time
        # the movie has shown up in the reommended list
        # return the value in the dictionary with the highest number of occurences

        liked_movies = self.get_liked(self.result_list)

        # lists of lists of recommended movies
        recommended_lists = []

        for liked in liked_movies:
            recommended_lists.append(self.get_recommended(liked))

        combine_recs = {}

        for each_rec_list in recommended_lists:
            for ele in each_rec_list:
                if (ele.id in combine_recs):
                    print("THERE HAS BEEN AN INCREMENTATION")
                    current_val = combine_recs[ele.id]
                    del combine_recs[ele.id]
                    combine_recs[ele.id] = current_val+1
                else:
                    combine_recs[ele.id] = 1

        print(combine_recs)

        result_id = max(combine_recs, key=combine_recs.get)

        # get data using API
        response = requests.get("https://api.themoviedb.org/3/movie/" + str(
            result_id) + "?api_key=3dbf9b55bdf367747f40974789edbff7&language=en-US")

        # convert data to dictionary
        dictionary = json.loads(response.text)

        # create movie object
        result = Movie(dictionary)

        return result
