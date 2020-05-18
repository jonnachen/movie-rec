import json


class Movie:
    def __init__(self, movie_dict):
        self.popularity = movie_dict["popularity"]
        self.vote_count = movie_dict["vote_count"]
        self.video = movie_dict["video"]
        self.poster_path = movie_dict["poster_path"]
        self.id = movie_dict["id"]
        self.adult = movie_dict["adult"]
        self.backdrop_path = movie_dict["backdrop_path"]
        self.original_language = movie_dict["original_language"]
        self.original_title = movie_dict["original_title"]
        self.genre_ids = movie_dict["genre_ids"]
        self.title = movie_dict["title"]
        self.vote_average = movie_dict["vote_average"]
        self.overview = movie_dict["overview"]
        self.release_date = movie_dict["release_date"]

    def get_string(self):
        json.dumps(self.__dict__)
