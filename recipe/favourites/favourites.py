from flask import Blueprint, render_template, redirect, url_for, flash, session
from recipe.auth.auth import login_required
import recipe.adapters.repository as repo
import recipe.auth.services as services

favourites_bp = Blueprint("favourites_bp", __name__, url_prefix="/favourites")


@favourites_bp.route("/")
def favourites():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must log in to view your favourites.", "warning")
        return redirect(url_for("auth_bp.login"))

    user = services.retrieve_user_by_id(user_id, repo.repo_instance)
    if not user:
        flash("User not found. Please log in again.", "danger")
        session.clear()
        return redirect(url_for("auth_bp.login"))

    return render_template("favourites/favourites.html", favourites=user.favourite_recipes)
