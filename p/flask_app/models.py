from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from collections import Counter



@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()
    interested_courses = db.ListField(db.StringField(), default=list)
    enrolled_courses = db.ListField(db.StringField(), default=list)
    interested_clubs = db.ListField(db.StringField(), default=list)
    enrolled_clubs = db.ListField(db.StringField(), default=list)
    following_people = db.ListField(db.ReferenceField('User'), default=list)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username
    
    # Returns courses the user might be interested in based on what their following have
    # Sorted by number of people interested/enrolled in 
    def potential_courses(self):
        courses = []
        current_user_courses = set(self.interested_courses)

        for user in self.following_people:
            courses.extend(c for c in user.interested_courses + user.enrolled_courses if c not in current_user_courses)

        course_counts = Counter(courses)
        sorted_courses = sorted(course_counts.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_courses
        


class Review(db.Document):
    commenter = db.ReferenceField('User')
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(unique=True, required=True)
    imdb_id = db.StringField(required=True, min_length=9, max_length=9)
    movie_title = db.StringField(required=True, min_length=1, max_length=100)
    image = db.StringField()
    #Uncomment when other fields are ready for review pictures