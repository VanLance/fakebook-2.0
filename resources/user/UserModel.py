from app import db
from werkzeug.security import generate_password_hash, check_password_hash

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('users.id'))
)

class UserModel(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100), unique = True, nullable = False)
  email = db.Column(db.String(100), unique = True, nullable = False)
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  password_hash = db.Column(db.String(), nullable = False)
  posts = db.relationship('PostModel', backref = 'author', lazy='dynamic', cascade='all, delete')
  following = db.relationship(
        'UserModel', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

  def __repr__(self):
    return f'<User: {self.username}>'
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def hash_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def from_dict(self, user_obj):
    for attribute, v in user_obj.items():
        setattr(self, attribute, v)

  def follow(self, user):
    if not self.is_following(user):
      self.following.append(user)

  def unfollow(self,user):
    if self.is_following(user):
      self.following.remove(user)

  def is_following(self, user):
        return self.following.filter(
            followers.c.following_id == user.id).count() > 0

