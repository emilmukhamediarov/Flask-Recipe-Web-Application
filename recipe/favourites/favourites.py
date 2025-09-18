from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

favourites_bp = Blueprint("favourites_bp", __name__, url_prefix="/favourites")

@favourites_bp.route("/")
@login_required
def favourites():
    favs = []
    return render_template("favourites/favourites.html", favourites=favs)