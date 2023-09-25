import os
from secrets import SystemRandom

class Config:
  PROPAGATE_EXCEPTIONS = True
  API_TITLE = "FakeBook REST API"
  API_VERSION = "v1"
  OPENAPI_VERSION = "3.0.3"
  OPENAPI_URL_PREFIX = "/"
  OPENAPI_SWAGGER_UI_PATH = "/"
  OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = 0
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')