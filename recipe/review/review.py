from flask import Blueprint, request, flash, redirect, url_for, session

from recipe.domainmodel.review import Review
import recipe.adapters.repository as repo
from recipe.review import services
from recipe.auth.auth import login_required
from recipe.review.services import UserNotFound, InvalidUser
from datetime import date

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/review', methods=['POST'])
@login_required
def review():
    user_id = session.get('user_id')
    recipe_id = int(request.form['recipe_id'])
    rating = int(request.form['rating'])
    text = request.form['text']
    created_date = date.today()

    if services.review_already_exists(user_id, recipe_id, repo.repo_instance):
        flash("You have already reviewed this recipe", "warning")
        return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))
    else:
        try:
            services.create_review(user_id, recipe_id, rating, text, created_date, repo.repo_instance)
            flash("Review successfully submitted", "success")
            return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))
        except UserNotFound:
            flash("User doesn't exist", "warning")
            return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))

@review_bp.route('/review/delete', methods=['POST'])
@login_required
def delete_review():
    review_id = int(request.form['review_id'])
    recipe_id = int(request.form['recipe_id'])
    user_id = session.get('user_id')
    try:
        services.delete_review(user_id, review_id, repo.repo_instance)
        flash("Review successfully deleted", "success")
    except InvalidUser:
        flash("You are not authorised to delete this review", "warning")
    return redirect(url_for('recipe_details_bp.get_recipe_details', recipe_id=recipe_id))

