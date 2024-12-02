import base64,io
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm, FollowForm, UnfollowForm
from ..models import User

users = Blueprint("users", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ User Management views ************ """


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('users.login'))
    return render_template('register.html', form = form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username = form.username.data).first()
            
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account'))
            else:
                flash("Login failed!")
    return render_template('login.html', form = form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            current_user.modify(username=update_username_form.username.data)
            current_user.save()

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            img = update_profile_pic_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'
            
            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
            current_user.save()
            return redirect(url_for('users.account'))
    profile_pic_bytes = BytesIO(current_user.profile_pic.read())
    profile_pic_base64 = base64.b64encode(profile_pic_bytes.getvalue()).decode()
    return render_template("account.html",update_username_form=update_username_form, update_profile_pic_form=update_profile_pic_form, profile_pic_base64 = profile_pic_base64)


@users.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user_detail(username):
    user = User.objects(username=username).first()
    
    if user is None:
        error_message = f"No user found"
        return render_template('user_detail.html', error=error_message)
    
    img = get_b64_img(user.username) 
    
    follow_form = FollowForm(prefix="follow")
    unfollow_form = UnfollowForm(prefix="unfollow")
    
    is_following = user in current_user.following_people

    if follow_form.submit_follow.data and follow_form.validate_on_submit():
        if not is_following:
            current_user.following_people.append(user)
            current_user.save()
            flash(f"You are now following {username}.", "success")
        return redirect(url_for("users.user_detail", username=username))

    if unfollow_form.submit_unfollow.data and unfollow_form.validate_on_submit():
        if is_following:
            current_user.following_people.remove(user)
            current_user.save()
            flash(f"You have unfollowed {username}.", "success")
        return redirect(url_for("users.user_detail", username=username))
    
    return render_template(
        'user_detail.html',
        image=img,
        follow_form=follow_form,
        unfollow_form=unfollow_form,
        follow=is_following
    )
