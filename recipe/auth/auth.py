from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
from recipe.domainmodel.user import User
import recipe.adapters.repository as repo
from recipe.auth.forms import LoginForm, RegisterForm
import recipe.auth.services as services

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# LoginManager setup
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"

@login_manager.user_loader
def load_user(user_id):
    return services.retrieve_user_by_id(user_id, repo.repo_instance)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = services.retrieve_user_by_name(form.username.data, repo.repo_instance)
        if user and user.check_password(form.password.data):
            login_user(user)
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
            new_user = User(username=form.username.data, password=form.password.data)
            services.add_new_user(new_user, repo.repo_instance)
            flash("Registration successful, please log in", "success")
            return redirect(url_for('auth_bp.login'))
    return render_template("auth/register.html", form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('home_bp.home'))