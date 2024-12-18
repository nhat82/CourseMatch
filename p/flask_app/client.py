import requests
# import planetterp as terp
import re
from PIL import Image
import base64
import io
from io import BytesIO
import json

'''
Separeate input string for search into 2 groups: Department and Course Number. 
If both are found, return the reformatted string for a course.
Else, return the reformatted string (upper case and no space)
'''
def separate_string(input_string):
    uppercase_string = input_string.upper()
    match = re.match(r"([A-Za-z]+)\s*(\d+)", uppercase_string)
    if match:
        letters = match.group(1)
        numbers = match.group(2)
        return letters + numbers, "Course"
    else:
        return uppercase_string, "Dept"

class Course(object):
    def __init__(self, terp_json):
        self.name = terp_json["name"]
        self.title = terp_json["title"]
        self.credits = terp_json["credits"]
        self.description = terp_json["description"]
        self.type = "Course"

    def __repr__(self):
        return self.name


class CourseClient(object):
    def __init__(self):
        self.sess = requests.Session()

    def search(self, search_string):
        """
        Searches the API for the supplied search_string, and returns
        a list of Course objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        reformatted_string, label = separate_string(search_string)
        if label == "Course":
            data = requests.get(f"https://api.planetterp.com/v1/course?name={reformatted_string}").json() #course
        else:
            data = requests.get(f"https://api.planetterp.com/v1/courses?department={reformatted_string}&limit=18").json() #department, limit 12 courses
        
        
        if 'error' in data and data["error"] == "course not found":
            raise ValueError(f"course {reformatted_string} not found")
        
        
        # check if it's not a list. if not, then there's only 1 result
        if not isinstance(data, list):
            return [data]
            
        result = []
        ## We may have more results than are first displayed
        for terp_json in data:
            if 'error' in terp_json and terp_json["error"] == "course not found":
                break
            
            result.append(Course(terp_json))
        return result

    def retrieve_course_by_id(self, course_name):
        """
        Use to obtain a Course object representing the course identified by
        the supplied course_name
        """
        reformatted_course_name, _ = separate_string(course_name)
        data = requests.get(f"https://api.planetterp.com/v1/course?name={reformatted_course_name}").json() #course

        if 'error' in data and data["error"] == "course not found":
            raise ValueError(f"course {reformatted_course_name} not found")

        course = Course(data)

        return course


class Club():
    def __init__(self):
        self.clubs = {}
        try:
            with open('clubs.json', 'r') as json_file:
                self.clubs = json.load(json_file)
        except:
            print('Error in reading club data')

    def size(self):
        return len(self.clubs)

    def __repr__(self):
        return json.dumps(self.clubs, indent=4)

    def search(self, search_string):
        if search_string in self.clubs:
            url = self.clubs[search_string]['img']
            # Fetch the image from the URL
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad status codes

            # Open the image using PIL
            image = Image.open(io.BytesIO(response.content))

            # Convert the image to bytes
            data = io.BytesIO()
            image.save(data, format="JPEG") 

            # Encode the bytes to Base64
            encoded_img_data = base64.b64encode(data.getvalue()).decode("utf-8")

            return [[search_string, self.clubs[search_string]['url'], self.clubs[search_string]['desc'], encoded_img_data]]
        return []



## -- Example usage -- ###
if __name__ == "__main__":
    x = "CMSC"
    y = "CMSC132"
    
    client = CourseClient()
    results = client.search(y)
    print(results[0])
    club_sample = Club()
    print(len(club_sample)) # 900+ clubs
    print(club_sample.search("Sudanese Student Organization")[0][1]) # Provides link for club
    # print(results)
    # c = results[0]
    # print(type(c))
    # course = client.retrieve_course_by_id(y)
    # print(course)
    # print(type(course))
    # print(course.name)
    # print(course.title)
    # print(course.credits)
    # print(course.description)

# import requests


# class Movie(object):
#     def __init__(self, omdb_json, detailed=False):
#         if detailed:
#             self.genres = omdb_json["Genre"]
#             self.director = omdb_json["Director"]
#             self.actors = omdb_json["Actors"]
#             self.plot = omdb_json["Plot"]
#             self.awards = omdb_json["Awards"]

#         self.title = omdb_json["Title"]
#         self.year = omdb_json["Year"]
#         self.imdb_id = omdb_json["imdbID"]
#         self.type = "Movie"
#         self.poster_url = omdb_json["Poster"]

#     def __repr__(self):
#         return self.title


# class CourseClient(object):
#     def __init__(self, api_key):
#         self.sess = requests.Session()
#         self.base_url = f"http://www.omdbapi.com/?apikey={api_key}&r=json&type=movie&"

#     def search(self, search_string):
#         """
#         Searches the API for the supplied search_string, and returns
#         a list of Media objects if the search was successful, or the error response
#         if the search failed.

#         Only use this method if the user is using the search bar on the website.
#         """
#         search_string = "+".join(search_string.split())
#         page = 1

#         search_url = f"s={search_string}&page={page}"

#         resp = self.sess.get(self.base_url + search_url)

#         if resp.status_code != 200:
#             raise ValueError(
#                 "Search request failed; make sure your API key is correct and authorized"
#             )

#         data = resp.json()

#         if data["Response"] == "False":
#             raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

#         search_results_json = data["Search"]
#         remaining_results = int(data["totalResults"])

#         result = []

#         ## We may have more results than are first displayed
#         while remaining_results != 0:
#             for item_json in search_results_json:
#                 result.append(Movie(item_json))
#                 remaining_results -= len(search_results_json)
#             page += 1
#             search_url = f"s={search_string}&page={page}"
#             resp = self.sess.get(self.base_url + search_url)
#             if resp.status_code != 200 or resp.json()["Response"] == "False":
#                 break
#             search_results_json = resp.json()["Search"]

#         return result

#     def retrieve_movie_by_id(self, imdb_id):
#         """
#         Use to obtain a Movie object representing the movie identified by
#         the supplied imdb_id
#         """
#         movie_url = self.base_url + f"i={imdb_id}&plot=full"

#         resp = self.sess.get(movie_url)

#         if resp.status_code != 200:
#             raise ValueError(
#                 "Search request failed; make sure your API key is correct and authorized"
#             )

#         data = resp.json()

#         if data["Response"] == "False":
#             raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

#         movie = Movie(data, detailed=True)

#         return movie


# ## -- Example usage -- ###
# if __name__ == "__main__":
#     import os

#     client = MovieClient(os.environ.get("OMDB_API_KEY"))

#     movies = client.search("guardians")

#     for movie in movies:
#         print(movie)

#     print(len(movies))
