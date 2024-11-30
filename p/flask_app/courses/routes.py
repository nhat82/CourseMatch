import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import course_client
from ..forms import SearchForm, AddCourseForm
from ..models import User, Review
from ..utils import current_time

courses = Blueprint("courses", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@courses.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("courses.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@courses.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = course_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))
    
    users = []
    if current_user.is_authenticated:
        users = User.objects(username = query)
        
    # return render_template("query.html", results=results, users = users)
    return render_template("query.html", results=results, users = users)


@courses.route("/courses/<course_name>", methods=["GET", "POST"])
def course_detail(course_name):
    try:
        result = course_client.retrieve_course_by_id(course_name)
        return render_template("course_detail.html", course=result)
    except ValueError as e:
        return render_template("course_detail.html", error_msg=str(e))
    
    # add_course_form = AddCourseForm()
    
    # if current_user.is_authenticated:
    #     if request.method == 'POST' and add_course_form.validate_on_submit():
    #         option = add_course_form.select_field.data
    #         if option == 'interested':
    #             if course_name not in current_user.interested_courses:
    #                 current_user.interested_courses.append(course_name)
    #         else:
    #             if course_name not in current_user.enrolled_courses:
    #                 current_user.enrolled_courses.append(course_name)
    #         current_user.save()
    #         return render_template("course_detail.html", course=result, add_course_form=add_course_form)
        
    # return redirect(url_for('courses.course_detail', course_name=result))


@courses.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    if user is None:
        error_message = f"No user found"
        return render_template('user_detail.html', error=error_message)
    
    img = get_b64_img(user.username) #use their username for helper function
    
    
    return render_template('user_detail.html',image=img)
