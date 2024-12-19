from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


# class MovieReviewForm(FlaskForm):
#     text = TextAreaField(
#         "Comment", validators=[InputRequired(), Length(min=5, max=500)]
#     )
#     submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField("Update")

    def validate_username(self, username):
        # check if the new username is already taken
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken, choose another name")


class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Choose file',  validators=[InputRequired(), FileAllowed(['png', 'jpg'])])
    submit_picture = SubmitField("Update")


class AddCourseForm(FlaskForm):
    choices = [('interested', 'Interested'), ('enrolled', 'Enrolled')]
    select_field = SelectField('Select an option', choices=choices)
    submit_add_course = SubmitField("Add Course!")
    

class RemoveCourseForm(FlaskForm):
    submit_remove_course = SubmitField("Remove Course!")
    # can only remove course if it's in the current user's list of courses added
    # def validate_remove(self, username):
        # get current user 
        # user = User.__objects(username=username.data).first()
        # check if the current course already added
        
        
class FollowForm(FlaskForm):
    submit_follow = SubmitField("Follow")
    
class UnfollowForm(FlaskForm):
    # can only unfollow if it's in the current user's list of following people
    submit_unfollow = SubmitField("Unfollow")

class AddClubForm(FlaskForm):
    choices = [('interested', 'Interested'), ('enrolled', 'Enrolled')]
    select_field = SelectField('Select an option', choices=choices)
    submit_add_club = SubmitField("Add Club!")

class RemoveClubForm(FlaskForm):
    submit_remove_club = SubmitField("Remove Club!")