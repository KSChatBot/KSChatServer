from flask import Response, request
from flask_jwt_extended import create_access_token
from database.models import User
from flask_restx import Resource, Namespace, fields
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError

Authentication_NS = Namespace(
    name="Authentication",
    description="사용자 Authentication 하기 위해 사용하는 API.",
)

user_fields = Authentication_NS.model('User', {  # Model 객체 생성
    'email': fields.String(description='a User ID', required=True, example="aa@aa.com"),
    'password': fields.String(description='The API_Content api_desc', required=True)
})

@Authentication_NS.route('/signup')
class SignupApi(Resource):
    @Authentication_NS.expect(user_fields)
    def post(self):
        try:
            body = request.get_json()
            user =  User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError

@Authentication_NS.route('/login')
class LoginApi(Resource):
    @Authentication_NS.expect(user_fields)
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError