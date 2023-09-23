from app import app, db
from resources.user.UserModel import UserModel
from resources.post.PostModel import PostModel

@app.shell_context_processor
def make_shell_context():
  return {'db':db, 'User':UserModel, 'Post':PostModel}