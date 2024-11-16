import requests
# import planetterp as terp
import re

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


class Client(object):
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
            data = requests.get(f"https://api.planetterp.com/v1/course?name={x}").json() #course
        else:
            data = requests.get(f"https://api.planetterp.com/v1/courses?department={x}&limit=3").json() #department, limit 3 courses

        result = []
        
        if 'error' in data and data["error"] == "course not found":
            raise ValueError(f"course {x} not found")
        
        ## We may have more results than are first displayed
        for terp_json in data:
            if 'error' in data and data["error"] == "course not found":
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
            raise ValueError(f"course {x} not found")

        course = Course(data)

        return course


## -- Example usage -- ###
if __name__ == "__main__":
    x = "CMSC"
    y = "CMSC132"
    
    client = Client()
    results = client.search(x)
    print(len(results))
    print(results)
    course = client.retrieve_course_by_id(y)
    print(course)
    print(course.description)

    
