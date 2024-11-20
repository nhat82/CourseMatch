import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import course_client
from ..forms import MovieReviewForm, SearchForm
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

    return render_template("query.html", results=results)


@courses.route("/courses/<course_name>", methods=["GET", "POST"])
def course_detail(course_name):
    try:
        result = course_client.retrieve_course_by_id(course_name)
    except ValueError as e:
        return render_template("course_detail.html", error_msg=str(e))

    # form = MovieReviewForm()
    # if form.validate_on_submit():
    #     review = Review(
    #         commenter=current_user._get_current_object(),
    #         content=form.text.data,
    #         date=current_time(),
    #         imdb_id=course_name,
    #         movie_title=result.title,
    #     )

    #     review.save()

    #     return redirect(request.path)

    # reviews = Review.objects(imdb_id=course_name)

    return render_template("course_detail.html", course=result)


@courses.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    if user is None:
        error_message = f"No user found"
        return render_template('user_detail.html', error=error_message)
    
    img = get_b64_img(user.username) #use their username for helper function
    user_reviews = list(Review.objects(commenter=current_user))
    num_user_reviews = len(user_reviews)
    return render_template('user_detail.html',image=img, num_user_reviews=num_user_reviews, user_reviews=user_reviews)
