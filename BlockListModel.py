from app import db

class BlockListModel(db.Model):

  id = db.Column(db.Integer, primary_key = True)
  token = db.Column(db.String(), nullable = False)

  def __repr__(self):
    return f'<Revoked Token: {self.token}'