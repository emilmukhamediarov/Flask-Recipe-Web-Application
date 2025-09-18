from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user

import recipe.adapters.repository as repo
from recipe.favourites import services
from recipe.domainmodel.favourite import Favourite

favourites_bp = Blueprint("favourites_bp", __name__, url_prefix="/favourites")

@favourites_bp.route("/", methods=["GET", "POST"])
@login_required
def favourites():
    if request.method == "POST":
        user_id = int(request.form["user_id"])
        recipe_id = int(request.form["recipe_id"])

        favourite = Favourite(user_id, recipe_id)
        services.add_new_favourite(favourite, repo.repo_instance)
        flash("Favourite has been added", "success")

        return redirect(url_for("recipe_details_bp.get_recipe_details", recipe_id=recipe_id))

    favourites = services.get_favourites(current_user.id, repo.repo_instance)
    return render_template("favourites/favourites.html", recipes=favourites)