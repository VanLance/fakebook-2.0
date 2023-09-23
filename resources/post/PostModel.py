from app import db
from datetime import datetime

class PostModel(db.Model):

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key = True)
  body = db.Column(db.String(), nullable = False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

  def __repr__(self):
    return f'<Post: {self.body}>'

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def from_dict(self, dict):
    for k, v in dict.items():
      setattr(self, k, v)