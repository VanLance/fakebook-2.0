from flask_smorest import Blueprint

bp = Blueprint('users', __name__, description='Operations on users')

from resources.user import routes