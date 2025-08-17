from flask import Blueprint, render_template

from recipe.adapters.repository import AbstractRepository
# .recipe_get_all()
browse_bp = Blueprint('browse_bp', __name__)

@browse_bp.route('/browse', methods=['GET'])
def browse():
    return render_template('samples/browse.html')