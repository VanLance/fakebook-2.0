from flask.views import MethodView
from flask_smorest import abort

from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from resources.user.UserModel import UserModel

from . import bp
from db import users,posts
from schemas import PlainUserSchema, PostSchema, UserUpdateSchema, UserSchema

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
  
  @jwt_required()
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

