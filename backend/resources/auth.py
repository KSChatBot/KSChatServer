from flask import Response, request, json, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from database.models import User, RevokedToken
from flask_restx import Resource, Namespace, fields
from datetime import timezone, datetime, timedelta
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, InvalidQueryError
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, UserAlreadyExistsError, \
InternalServerError, UpdatingUserError, DeletingUserError, UserNotExistsError
from database.db import db

# import sys, os

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from app import jwt

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
    'password': fields.String(description='a User Password', required=True, example="영숫자, 특수문자 조합 6문자 이상으로..."),
    'title': fields.String(description='a User Title', required=True, example="Mr 또는 Mrs, Miss, Ms"),
    'firstName': fields.String(description='a User firstName', required=True),
    'lastName': fields.String(description='a User lastName', required=True),
    'role': fields.String(description='a User Role', required=True, example="User 또는 Admin"),
    'acceptTerms': fields.Boolean(description='a User acceptTerms', example="True 또는 False")
})

user_authentication_fields = Authentication_NS.model('User_Authentication', {  # Model 객체 생성
    'email': fields.String(description='a User Email', required=True, example="aa@aa.com"),
    'password': fields.String(description='a User Password', required=True)
})

user_fields_with_id = Authentication_NS.inherit('User With ID', user_fields, {
    'email': fields.String(description='a User Email', example="aa@aa.com")
})

@Authentication_NS.route('/register')
class SignupApi(Resource):
    @Authentication_NS.expect(user_fields)
    def post(self):
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======data_dict=======")
            print(data_dict)
            print("======end data_dict=======")
# {'title': 'Mr', 'firstName': 'aa', 'lastName': 'bb', 'email': 'aa@aa.com', 'password': '123456', 'confirmPassword': '123456', 'acceptTerms': True}
            user = User()
            user.title = data_dict.get('title')
            user.firstName = data_dict.get('firstName')
            user.lastName = data_dict.get('lastName')
            user.email = data_dict.get('email')
            user.role = data_dict.get('role')
            # 필드명 주의
            user.password = data_dict.get('password')
            user.acceptTerms = data_dict.get('acceptTerms')
            user.hash_password()
            firstUser = User.objects().first()
            if firstUser:
                if user.role is None:
                    user.role = 'User'
            else:
                user.role = 'Admin'
            user.save()
            id = user.id

            print("사용자 등록 성공....")

            return {'email': data_dict.get('email')}, 200

        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError

@Authentication_NS.route('/authenticate')
class LoginApi(Resource):
    @Authentication_NS.expect(user_authentication_fields)
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            refresh_token = create_refresh_token(identity=str(user.id))

            print("로그인 성공....")

            return { 'id': str(user.id),
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

@Authentication_NS.route('/revoke-token')
class UserLogoutAccess(Resource):
    """
    User Logout Api 
    """

    @jwt_required()
    def post(self):

        jti = get_jwt()['jti']
        try:
            # Revoking access token
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            print("로그아웃 성공....")
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

@Authentication_NS.route('/refresh-token')
class TokenRefresh(Resource):
    """
    Token Refresh Api
    """
    @jwt_required(refresh=True)
    def post(self):

        # Generating new access token
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user)
        refresh_token = create_refresh_token(current_user)
        print("토큰 리프레쉬....")
        return {'jwtToken': access_token,
                'refreshToken': refresh_token}, 200


@Authentication_NS.route('')
class UserListApi(Resource):
    """
    모든 사용자 조회 Api
    """
    @Authentication_NS.doc('list_users')
    def get(self):
        query = User.objects()
        users = User.objects().to_json()
        print("사용자정보 전부 query 성공....")

        return Response(users, mimetype="application/json", status=200)


@Authentication_NS.route('/<string:email>')
class UserApi(Resource):
    """
    사용자 정보 수정 삭제 조회 Api
    """
    @Authentication_NS.expect(user_fields)
    @Authentication_NS.response(202, 'Success', user_fields_with_id)
    @Authentication_NS.response(500, 'Failed')
    def put(self, email):
        """
        사용자 정보 수정 Api
        """
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======수정할사용자정보=======")
            print(data_dict)
            print("======end 수정할사용자정보=======")
            user = User.objects.get(email=email)
            user.title = data_dict.get('title')
            user.firstName = data_dict.get('firstName')
            user.lastName = data_dict.get('lastName')
            user.email = data_dict.get('email')

            # 사용자 Role 처리
            if data_dict.get('role'):
                user.role = data_dict.get('role')
            
            user.acceptTerms = data_dict.get('acceptTerms')
            # 비밀번호 입력시 처리
            if data_dict.get('password'):
                user.password = data_dict.get('password')
                user.hash_password()

            user.save()
            id = user.id

            print("사용자정보 수정 성공....")

            return { 'id': str(user.id),
                     'email': user.email,
                     'title': user.title,
                     'firstName': user.firstName,
                     'lastName': user.lastName,
                     'role': user.role
                    }, 200

        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingUserError
        except Exception:
            raise InternalServerError       
    
    @Authentication_NS.doc(params={'email': 'An Email'})
    @Authentication_NS.doc(responses={202: 'Success'})
    @Authentication_NS.doc(responses={500: 'Failed'})
    def delete(self, email):
        """
        사용자 정보 삭제 Api
        """
        try:
            user = User.objects.get(email=email)
            user.delete()
            print("사용자정보 삭제 성공....")

            return '', 200
        except DoesNotExist:
            raise DeletingUserError
        except Exception:
            raise InternalServerError

    @Authentication_NS.doc(params={'email': 'An Email'})
    @Authentication_NS.response(200, 'Success', user_fields_with_id)
    @Authentication_NS.response(500, 'Failed')
    def get(self, email):
        """
        사용자 정보 조회 Api
        """
        try:
            user = User.objects.get(email=email).to_json()
            print("사용자정보 조회 성공....")
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
