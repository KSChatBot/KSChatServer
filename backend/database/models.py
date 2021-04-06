from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class API_Content(db.Document):
    api_name = db.StringField(required=True, unique=True)
    api_desc = db.StringField()
    api_key = db.StringField()
    api_endpoint = db.StringField()
    api_data_format = db.StringField()
    added_by = db.ReferenceField('User')

class ResetToken(db.EmbeddedDocument):
    token = db.StringField()
    expires = db.DateTimeField()


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    passwordHash = db.StringField(required=True)
    title = db.StringField(required=True)
    firstName = db.StringField(required=True)
    lastName = db.StringField(required=True)
    acceptTerms = db.BooleanField()
    role = db.StringField(required=True)
    verificationToken = db.StringField()
    verified = db.DateTimeField()
    resetToken = db.EmbeddedDocumentField(ResetToken)
    passwordReset = db.DateTimeField()
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    updated = db.DateTimeField()
    api_contents = db.ListField(db.ReferenceField('API_Content', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.passwordHash = generate_password_hash(self.passwordHash).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

User.register_delete_rule(API_Content, 'added_by', db.CASCADE)