from flask import Response, request
from flask_jwt_extended import create_access_token, create_refresh_token
from database.models import User
from flask_restx import Resource, Namespace, fields
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, MovieAlreadyExistsError, \
InternalServerError

Authentication_NS = Namespace(
    name="Accounts Authentication",
    description="사용자 Authentication 하기 위해 사용하는 API.",
)
resetToken_fields = Authentication_NS.model('ResetToken', {
    'token': fields.String,
    'expires': fields.DateTime,
})

user_fields = Authentication_NS.model('User', {  # Model 객체 생성
    'email': fields.String(description='a User Email', required=True, example="aa@aa.com"),
    'passwordHash': fields.String(description='a User Password', required=True),
    'title': fields.String(description='a User Title', required=True),
    'firstName': fields.String(description='a User firstName', required=True),
    'lastName': fields.String(description='a User lastName', required=True),
    'acceptTerms': fields.Boolean(description='a User acceptTerms'),
    'role': fields.String(description='a User role', required=True),
    'verificationToken': fields.String(description='a User verificationToken'),
    'verified': fields.DateTime(description='a User verified'),
    # 'resetToken': fields.String(fields.Nested(resetToken_fields), description='a User resetToken'),
    'passwordReset': fields.DateTime(description='a User passwordReset'),
    'updated': fields.DateTime(description='a User updated')
})

user_fields_with_id = Authentication_NS.inherit('User With ID', user_fields, {
    'id': fields.Integer(description='a User ID')
})


@Authentication_NS.route('/register')
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

@Authentication_NS.route('/authenticate')
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
            refresh_token = create_refresh_token(user.id)

            return { 'id': user.id,
                     'email': user.email,
                     'title': user.title,
                     'firstName': user.firstName,
                     'lastName': user.lastName,
                     'role': user.role,
                     'jwtToken': access_token,
                     'refreshToken': refresh_token
                    }, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError

@Authentication_NS.route('/refresh-token')
class TokenRefresh(Resource):
    @Authentication_NS.expect(user_fields)
    def post(self):
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        refresh_token = create_refresh_token(current_user)
        return {'jwtToken': new_token,
                'refreshToken': refresh_token}, 200


@Authentication_NS.route('')
class UserListApi(Resource):
    @Authentication_NS.doc('list_users')
    def get(self):
        query = User.objects()
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)


@Authentication_NS.route('/<int:id>')
@Authentication_NS.doc(params={'id': 'An ID'})
class UserApi(Resource):
    @Authentication_NS.response(202, 'Success', user_fields_with_id)
    @Authentication_NS.response(500, 'Failed')
    def put(self, id):
        try:
            body = request.get_json()
            User.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError       
    
    @Authentication_NS.doc(responses={202: 'Success'})
    @Authentication_NS.doc(responses={500: 'Failed'})
    def delete(self, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    @Authentication_NS.response(200, 'Success', user_fields_with_id)
    @Authentication_NS.response(500, 'Failed')
    def get(self, id):
        try:
            user = User.objects.get(id=id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError
