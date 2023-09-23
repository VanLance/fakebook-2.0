from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from resources.post.PostModel import PostModel

from . import bp
from db import posts
from schemas import PostSchema, PostUpdateSchema
from resources.post.PostModel import PostModel

@bp.route('/post/<post_id>')
class Post(MethodView):
  
  @bp.response(200, PostSchema)
  def get(self, post_id):
    post = PostModel.query.get_or_404(post_id)
    return post

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
  
  @bp.response(200, PostSchema(many=True))
  def get(self):
    return PostModel.query.all()

  @bp.arguments(PostSchema)
  @bp.response(201, PostSchema)
  def post(self, post_data):
    try:
      post = PostModel(**post_data)
      post.save()    
    except:
      abort(500,message="Error occured while creating Post")
    return post