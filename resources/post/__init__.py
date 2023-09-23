from flask_smorest import Blueprint

bp = Blueprint('posts', __name__, description='Operations on posts')

from resources.post import routes