class Recommender:
    def __init__(self, result_list):
        self.result_list = result_list

    def safe_first_ele(self, result_list):
        if len(result_list) == 0:
            return None
        else:
            return (result_list[0])[0]
    # be sure to guard against error for if the result list passed in is empty

    def get_result(self):
        # dummy function for now -- only returns the first MOVIE object
        return self.safe_first_ele(self.result_list)
