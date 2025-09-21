from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_required

from recipe.domainmodel.review import Review
import recipe.adapters.repository as repo
from recipe.review import services

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/review', methods=['POST'])
@login_required
def review():
    user_id = int(request.form['user_id'])
    recipe_id = int(request.form['recipe_id'])
    rating = int(request.form['rating'])
    text = request.form['text']

    review = Review(user_id, recipe_id, rating, text)

    services.add_review(review, repo.repo_instance)
    flash("Review successfully submitted", "success")
    return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))



