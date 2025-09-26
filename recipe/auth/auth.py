from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash

from recipe.domainmodel.user import User
import recipe.adapters.repository as repo
from recipe.auth.forms import LoginForm, RegisterForm
import recipe.auth.services as services
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth_bp.login"))
        return view_func(**kwargs)
    return wrapped_view

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = services.retrieve_user_by_name(form.username.data, repo.repo_instance)

        if user and user.check_password(form.password.data):
            session.clear()
            session["username"] = user.username
            session["user_id"] = user.id

            flash("Logged in successfully!", "success")
            return redirect(url_for('home_bp.home'))

        flash("Invalid username or password", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if services.retrieve_user_by_name(form.username.data, repo.repo_instance):
            flash("Username already exists", "danger")
        else:
            username = form.username.data
            password = form.password.data
            new_user = User(username, password)
            services.add_new_user(new_user, repo.repo_instance)

            session.clear()
            session["username"] = new_user.username
            session["user_id"] = new_user.id

            flash("Registration successful! You are now logged in.", "success")
            return redirect(url_for('home_bp.home'))

    return render_template("auth/register.html", form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('home_bp.home'))
