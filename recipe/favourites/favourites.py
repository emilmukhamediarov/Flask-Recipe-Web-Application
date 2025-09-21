from flask import Blueprint, render_template, request, url_for, redirect, flash, session

from recipe.auth.auth import login_required

import recipe.adapters.repository as repo
from recipe.favourites import services
from recipe.domainmodel.favourite import Favourite

favourites_bp = Blueprint("favourites_bp", __name__, url_prefix="/favourites")

@favourites_bp.route("/", methods=["GET", "POST"])
@login_required
def favourites():
    user_id = session.get("user_id")
    if request.method == "POST":
        recipe_id = int(request.form["recipe_id"])

        try:
            services.create_favourite(user_id, recipe_id, repo.repo_instance)
            flash("Favourite has been added", "success")
            return redirect(url_for("recipe_details_bp.get_recipe_details", recipe_id=recipe_id))

        except services.UserNotFound:
            flash("User doesn't exist", "warning")
            return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))

    recipes = services.get_favourites(user_id, repo.repo_instance)
    return render_template("favourites/favourites.html", recipes=recipes)

@favourites_bp.route("/remove", methods=["POST"])
@login_required
def remove():
    user_id = session.get("user_id")
    recipe_id = int(request.form["recipe_id"])
    try:
        services.remove_favourite(user_id, recipe_id, repo.repo_instance)
        flash("Favourite has been removed", "success")
        return redirect(url_for("recipe_details_bp.get_recipe_details", recipe_id=recipe_id))
    except services.UserNotFound:
        flash("User doesn't exist", "warning")
        return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))
