from marshmallow import Schema, fields

class PostSchema(Schema):
  id = fields.Str(dump_only=True)
  body = fields.Str(required=True)
  user_id = fields.Str(required=True)

class PostUpdateSchema(Schema):
  body = fields.Str(required=True)

class PlainUserSchema(Schema):
  id = fields.Str(dump_only=True)
  username = fields.Str(required=True)
  email = fields.Str()
  password = fields.Str(required=True)

class UserUpdateSchema(Schema):
  username = fields.Str()
  email = fields.Str()

class UserSchema(PlainUserSchema):
  posts = fields.List(fields.Nested(PostSchema()), dump_only = True)
  following = fields.List(fields.Nested(PlainUserSchema()), dump_only = True)

