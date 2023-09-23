from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from BlockListModel import BlockListModel

from resources.user.UserModel import UserModel

from . import bp
from db import users,posts
from schemas import PlainUserSchema, PostSchema, UserUpdateSchema, UserSchema


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


@bp.route('/user/<user_id>')
class User(MethodView):

  @bp.response(200, UserSchema)
  def get(self,user_id):
    user = UserModel.query.get_or_404(user_id)
    return user

  def delete(self,user_id):
    user = UserModel.query.get_or_404(user_id)
    user.delete()
    return {'message':f'{user.username } Deleted'}

@bp.route('/user')
class UserList(MethodView):

  @bp.response(200, PlainUserSchema(many=True))
  def get(self):
    return UserModel.query.all()


@bp.get('/user/<user_id>/post')
@bp.response(200, PostSchema(many=True))
def get_user_posts(user_id):
  return UserModel.query.get(user_id).posts

@bp.route('/user/follow/<user_id>/<user_follow_id>')
class UserFollow(MethodView):

  @bp.response(201, UserSchema)
  def post(self, user_id, user_follow_id):
    user = UserModel.query.get(user_id)
    follow_user = UserModel.query.get(user_follow_id)
    if user and follow_user:
      user.follow(follow_user)
      user.save()
      return user
    else:
      abort(400, message = 'User not found')
  
  @bp.response(200, UserSchema)
  def put(self, user_id, user_follow_id):  
    user = UserModel.query.get(user_id)
    unfollow_user = UserModel.query.get(user_follow_id)
    if user and unfollow_user:
      user.unfollow(unfollow_user)
      user.save()
      return user
    else:
      abort(400, message = 'User not found')

@bp.route('/login')
class UserLogin(MethodView):
  @bp.arguments(PlainUserSchema)
  def post(self, user_data):
    user = UserModel.query.filter(username = user_data['username']).first()
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