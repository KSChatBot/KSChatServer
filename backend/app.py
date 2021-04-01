from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from database.db import initialize_db
# from flask_restful import Api
from flask_restplus import Api
from resources.errors import errors
import os

app = Flask(__name__)
# app.config.from_envvar('ENV_FILE_LOCATION')
#SMTP email server 설정
app.config.update(dict(
    DEBUG = True,
    # in this part I am introduicing my email as sender
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=  587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL= False,
    MAIL_USERNAME = 'abc@gmail.com',
    MAIL_PASSWORD = '**********',
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
))

mail = Mail(app)

# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
#몽고디비 설정
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ['MONGODB_HOST'],
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD'],
    'db': 'webapp'
}

initialize_db(app)
initialize_routes(api)
