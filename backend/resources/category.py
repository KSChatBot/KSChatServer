from flask import Response, request, json, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from database.models import Categories, User
from flask_restx import Resource, Namespace, fields
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from .errors import SchemaValidationError, CategoriesAlreadyExistsError, InternalServerError, \
UpdatingCategoriesError, DeletingCategoriesError, CategoriesNotExistsError
import datetime

Categories_NS = Namespace(
    name="Categories",
    description="Content API를 그룹화 하기위한 분류정보 Category를 작성하기 위해 사용하는 API.",
)

category_fields = Categories_NS.model('Categories', {  # Model 객체 생성
    'name': fields.String(description='a category', required=True, example="API의 그룹정보, UiPath_Orchestrator, ChatBot정보"),
    'desc': fields.String(description='The Categories description')
})

category_fields_with_id = Categories_NS.inherit('Categories With ID', category_fields, {
    'id': fields.String(description='a Categories ID')
})

@Categories_NS.route('')
class CategoriesBaseApi(Resource):
    @Categories_NS.doc('list_categorys')
    def get(self):
        query = Categories.objects()
        categories = Categories.objects().to_json()
        print("API Categories 조회 성공 ...")
        return Response(categories, mimetype="application/json", status=200)

    @Categories_NS.expect(category_fields)
    @Categories_NS.response(201, 'Success', category_fields_with_id)
    @jwt_required()
    def post(self):
        print("API Categories 등록 시작 ...")
        try:
            # 사용자 인증 체크, 로그인 되지 안으면 FieldDoesNotExist Exception 발생
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)

            data_json = request.data
            data_dict = json.loads(data_json)
            print("======API Categories 등록 정보=======")
            print(data_dict)
            print("======end API Categories 등록 정보=======")
            # category =  Categories(**body, added_by=user)
            category =  Categories()
            category.name = data_dict.get('name')
            category.desc = data_dict.get('desc')
            category.seq = Categories.objects.count() + 1
            category.updated  = datetime.datetime.utcnow          
            category.save()
            print("API Categories 등록 성공 ...")
            return { 'id': str(category.id),
                     'name': category.name,
                     'desc': category.desc,
                     'seq': category.seq
                    }, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise CategoriesAlreadyExistsError
        except Exception as e:
            raise InternalServerError

@Categories_NS.route('/<id>')
@Categories_NS.doc(params={'id': 'An ID'})
class CategoriesApi(Resource):
    @Categories_NS.response(202, 'Success', category_fields_with_id)
    @Categories_NS.response(500, 'Failed')
    @jwt_required()
    def put(self, id: str):
        print("API Categories 수정 시작 ...")
        try:
            # 사용자 인증 체크, 로그인 되지 안으면 FieldDoesNotExist Exception 발생
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)

            data_json = request.data
            data_dict = json.loads(data_json)
            print("======API Categories 수정 정보=======")
            print(data_dict)
            print("======end API Categories 수정 정보=======")
            category = Categories.objects.get(id=id)
            # category.name = data_dict.get('name')
            category.desc = data_dict.get('desc')
            category.updated  = datetime.datetime.utcnow          
            category.save()
            print("API Categories 수정 성공 ...")
            return { 'id': str(category.id),
                     'name': category.name,
                     'desc': category.desc,
                     'seq': category.seq
                    }, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingCategoriesError
        except Exception:
            raise InternalServerError       
    
    @Categories_NS.doc(responses={202: 'Success'})
    @Categories_NS.doc(responses={500: 'Failed'})
    @jwt_required()
    def delete(self, id: str):
        print("API Categories 삭제 시작 ...")
        try:
            # 사용자 인증 체크, 로그인 되지 안으면 FieldDoesNotExist Exception 발생
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            category = Categories.objects.get(id=id)
            category.delete()
            print("API Categories id={} 삭제 성공 ...".format(id))
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise DeletingCategoriesError
        except Exception:
            raise InternalServerError

    @Categories_NS.response(200, 'Success', category_fields_with_id)
    @Categories_NS.response(500, 'Failed')
    def get(self, id: str):
        print("API Categories 조회 시작 ...")
        try:
            category = Categories.objects.get(id=id).to_json()
            print("API Categories id={} 조회 성공 ...".format(id))
            return Response(category, mimetype="application/json", status=200)
        except DoesNotExist:
            raise CategoriesNotExistsError
        except Exception:
            raise InternalServerError

