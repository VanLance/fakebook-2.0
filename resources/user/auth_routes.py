from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_smorest import abort

from . import bp
from schemas import PlainUserSchema
from .UserModel import UserModel
from BlockListModel import BlockListModel


@bp.route('/register')
class UserRegister(MethodView):
  @bp.arguments(PlainUserSchema)
  @bp.response(201, PlainUserSchema)
  def post(self, user_data):
    try:
      user = UserModel()
      user.from_dict(user_data)
      user.hash_password(user.password)
      user.save()
    except IntegrityError:
      abort(400, message = "User with that username or email already exists")
    except:
      abort(400, message = "Error occured while creating user")
    del user.password
    return user
  
@bp.route('/login')
class UserLogin(MethodView):
  @bp.arguments(PlainUserSchema)
  def post(self, user_data):
    user = UserModel.query.filter_by(username = user_data['username']).first()
    if user and user.check_password(user_data['password']):
      access_token = create_access_token(identity=user.id)
      return {'access_token': access_token}, 200
    abort(401, message='Invalid Username/Password') 

@bp.route('/logout')
class UserLogOut(MethodView):
  @jwt_required()
  def post(self):
    revoked = BlockListModel(token = get_jwt()['jti'])
    revoked.save()
    return {"message": "Successfully logged out"}, 200