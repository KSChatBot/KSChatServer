from flask import request, render_template
from flask_jwt_extended import create_access_token, decode_token
from database.models import User
from flask_restx import Resource, Namespace, fields
import datetime
from resources.errors import SchemaValidationError, InternalServerError, \
    EmailDoesnotExistsError, BadTokenError
from jwt.exceptions import ExpiredSignatureError, DecodeError, \
    InvalidTokenError
from services.mail_service import send_email

Password_NS = Namespace(
    name="Password Management",
    description="사용자의 비밀번호를 관리 하기 위해 사용하는 API.",
)

@Password_NS.route('/forgot')
class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                raise SchemaValidationError

            user = User.objects.get(email=email)
            if not user:
                raise EmailDoesnotExistsError

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user.id), expires_delta=expires)

            return send_email('[KSChat Portal] Reset Your Password',
                              sender='support@movie-bag.com',
                              recipients=[user.email],
                              text_body=render_template('email/reset_password.txt',
                                                        url=url + reset_token),
                              html_body=render_template('email/reset_password.html',
                                                        url=url + reset_token))
        except SchemaValidationError:
            raise SchemaValidationError
        except EmailDoesnotExistsError:
            raise EmailDoesnotExistsError
        except Exception as e:
            raise InternalServerError


@Password_NS.route('/reset')
class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')

            if not reset_token or not password:
                raise SchemaValidationError

            user_id = decode_token(reset_token)['identity']

            user = User.objects.get(id=user_id)

            user.modify(password=password)
            user.hash_password()
            user.save()

            return send_email('[KSChat Portal] Password reset successful',
                              sender='support@movie-bag.com',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

        except SchemaValidationError:
            raise SchemaValidationError
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception as e:
            raise InternalServerError