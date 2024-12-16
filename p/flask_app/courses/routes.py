import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required

from .. import course_client, club
from ..forms import AddClubForm, RemoveClubForm, SearchForm, AddCourseForm, RemoveCourseForm
from ..models import User, Review
from ..utils import current_time

courses = Blueprint("courses", __name__)

""" ************ View functions ************ """


@courses.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("courses.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@courses.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    # print(len(club.clubs)) # 950
    is_course = False
    try:
        if query in club.clubs:
            results = club.search(query)
        else:
            is_course = True
            results = course_client.search(query)

    except ValueError as e:
        return render_template("query.html", error_msg=str(e))
    
    users = []
    if current_user.is_authenticated:
        users = User.objects(username = query)

    # print(results) 
    # return render_template("query.html", results=results, users = users)
    return render_template("query.html", results=results, users = users, course=is_course)


@courses.route("/courses/<course_name>", methods=["GET", "POST"])
def course_detail(course_name):
    try:
        result = course_client.retrieve_course_by_id(course_name)
        # return render_template("course_detail.html", course=result)
    except ValueError as e:
        return render_template("course_detail.html", error_msg=str(e))

    return render_template("course_detail.html", course=result, current_user = current_user)

@courses.route("/courses/club/<club_name>", methods=["GET", "POST"])
def club_detail(club_name):
    try:
        result = club.search(club_name)
        # return render_template("course_detail.html", course=result)
    except ValueError as e:
        return render_template("club_detail.html", error_msg=str(e))

    return render_template("club_detail.html", club=result, current_user = current_user)


@courses.route("/add_course/<course_name>", methods=["GET", "POST"])
@login_required
def add_course(course_name):
    form = AddCourseForm()
    course = course_name.strip()
    
    if form.validate_on_submit():
       
        type = form.select_field.data
        if type == "interested":
            if course not in current_user.interested_courses:
                current_user.interested_courses.append(course)
                flash(f"'{course}'  added to Interested Courses.")
            else:
                flash(f"'{course_name}' is already in your Interested Courses.", "error")
        elif type == "enrolled":
            if course not in current_user.enrolled_courses:
                current_user.enrolled_courses.append(course)
                flash(f"'{course}'  added to enrolled Courses.")
            else:
                flash(f"'{course_name}' is already in your Enrolled Courses.", "error")
        current_user.save()
        return redirect(url_for("courses.index"))
    return render_template("add_course.html", form=form, course_name=course, current_user = current_user)


@courses.route("/remove_course/<course_name>", methods=["GET", "POST"])
@login_required
def remove_course(course_name):
    form = RemoveCourseForm()  # Create the form instance
    course = course_name.strip()

    if form.validate_on_submit():  # Check if the form was submitted correctly
        

        # Check if course exists in user's lists
        if course_name in current_user.interested_courses:
            current_user.interested_courses.remove(course_name)
        elif course_name in current_user.enrolled_courses:
            current_user.enrolled_courses.remove(course_name)
        else:
            flash("Course not found in your list!", "error")
            return redirect(url_for("courses.index"))

        # Save changes to the database
        current_user.save()
        flash("Course removed successfully!", "success")
        return redirect(url_for("courses.index"))

    return render_template("remove_course.html", form=form, course_name=course)

@courses.route("/add_club/<club_name>", methods=["GET", "POST"])
@login_required
def add_club(club_name):
    form = AddClubForm()
    club = club_name
    
    if form.validate_on_submit():
       
        type = form.select_field.data
        if type == "interested":
            if club not in current_user.interested_clubs:
                current_user.interested_clubs.append(club)
                flash(f"'{club}'  added to Interested Clubs.")
            else:
                flash(f"'{club}' is already in your Interested Clubs.", "error")
        elif type == "enrolled":
            if club not in current_user.enrolled_clubs:
                current_user.enrolled_clubs.append(club)
                flash(f"'{club}'  added to enrolled club.")
            else:
                flash(f"'{club}' is already in your Enrolled Clubs.", "error")
        current_user.save()
        return redirect(url_for("courses.index"))
    return render_template("add_club.html", form=form, club_name=club, current_user = current_user)

@courses.route("/remove_club/<club_name>", methods=["GET", "POST"])
@login_required
def remove_club(club_name):
    form = RemoveClubForm()  # Create the form instance
    club = club_name

    if form.validate_on_submit():  # Check if the form was submitted correctly
        # Check if course exists in user's lists
        if club in current_user.interested_clubs:
            current_user.interested_clubs.remove(club)
        elif club in current_user.enrolled_clubs:
            current_user.enrolled_clubs.remove(club)
        else:
            flash("Club not found in your list!", "error")
            return redirect(url_for("courses.index"))

        # Save changes to the database
        current_user.save()
        flash("Club removed successfully!", "success")
        return redirect(url_for("courses.index"))

    return render_template("remove_club.html", form=form, club_name=club)
