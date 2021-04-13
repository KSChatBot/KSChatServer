from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class API_Content(db.Document):
    api_name = db.StringField(required=True, unique=True)
    api_desc = db.StringField()
    api_key = db.StringField()
    api_endpoint = db.StringField()
    api_data_format = db.DateTimeField(default=datetime.datetime.utcnow)
    ID = db.IntField(min_value=1)
    added_by = db.ReferenceField('User')

class ResetToken(db.EmbeddedDocument):
    token = db.StringField()
    expires = db.DateTimeField()

class RevokedToken(db.Document):
    """
    Revoked Token Model Class
    """
    __tablename__ = 'revoked_tokens'

    jti = db.StringField()

    """
    Save Token in DB
    """
    def add(self):

        db.session.add(self)

        db.session.commit()

    """
    Checking that token is blacklisted
    """
    @classmethod
    def is_jti_blacklisted(cls, jti):

        query = cls.query.filter_by(jti=jti).first()

        return bool(query)

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
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
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(API_Content, 'added_by', db.CASCADE)