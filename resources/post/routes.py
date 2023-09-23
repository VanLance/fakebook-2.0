from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt

from resources.post.PostModel import PostModel

from . import bp
from schemas import PostSchema, PostUpdateSchema
from resources.post.PostModel import PostModel

@bp.route('/post/<post_id>')
class Post(MethodView):
  
  @jwt_required()
  @bp.response(200, PostSchema)
  def get(self, post_id):
    post = PostModel.query.get_or_404(post_id)
    return post

  @jwt_required()
  def delete(self, post_id):
    post = PostModel.query.get_or_404(post_id)
    post_body = post.body
    post.delete()
    return f'Post: {post_body} deleted'

  @bp.arguments(PostUpdateSchema)
  @bp.response(200, PostSchema)
  def put(self, post_data, post_id):
    # post_data = request.get_json()
    # if 'body' not in post_data:
    #   abort(400,message='Please include body')
    post = PostModel.query.get_or_404(post_id)
    post.body = post_data['body']
    post.save()
    return post

@bp.route('/post')
class PostList(MethodView):
  
  @jwt_required()
  @bp.response(200, PostSchema(many=True))
  def get(self):
    jwt = get_jwt()
    return PostModel.query.all()

  @jwt_required()
  @bp.arguments(PostSchema)
  @bp.response(201, PostSchema)
  def post(self, post_data):
    try:
      post = PostModel(**post_data)
      post.save()    
    except:
      abort(500,message="Error occured while creating Post")
    return post