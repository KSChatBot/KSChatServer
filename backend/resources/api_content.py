from flask import Response, request, json, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from database.models import Contents, User, Categories
from flask_restx import Resource, Namespace, fields
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, ContentsAlreadyExistsError, InternalServerError, \
UpdatingContentsError, DeletingContentsError, ContentsNotExistsError
import datetime

Contents_NS = Namespace(
    name="Contents",
    description="Contents API 정보를 작성하기 위해 사용하는 API.",
)

api_content_fields = Contents_NS.model('Contents', {  # Model 객체 생성
    'api_name': fields.String(description='a Contents', required=True, example="날씨정보"),
    'api_desc': fields.String(description='The Contents api_desc', example="공공데이타날씨정보"),
    'api_endpoint': fields.String(description='The Contents api_endpoint'),
    'api_key': fields.String(description='The Contents api_key'),
    'api_ref1': fields.String(description='The Contents user definition api_ref1 field', example="사용자정의 필드1"),
    'api_ref2': fields.String(description='The Contents user definition api_ref2 field'),
    'api_ref3': fields.String(description='The Contents user definition api_ref3 field'),
    'api_ref4': fields.String(description='The Contents user definition api_ref4 field'),
    'api_ref5': fields.String(description='The Contents user definition api_ref5 field'),
    'category_id': fields.String(description='The Categories id(String)', required=True), 
    'api_data_format': fields.String(description='The Contents api_data_format') 
})

api_content_fields_with_id = Contents_NS.inherit('Contents With ID', api_content_fields, {
    'id': fields.String(description='a Contents ID')
})

@Contents_NS.route('')
class ContentsBaseApi(Resource):
    @Contents_NS.doc('list_api_contents')
    def get(self):
        query = Contents.objects()
        apicontents = Contents.objects().to_json()
        print("API Contents 조회 성공 ...")
        return Response(apicontents, mimetype="application/json", status=200)

    @Contents_NS.expect(api_content_fields)
    @Contents_NS.response(201, 'Success', api_content_fields_with_id)
    @jwt_required()
    def post(self):
        print("API Contents 등록 시작 ...")
        try:
            user_id = get_jwt_identity()
            # body = request.get_json()
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======API Contents 등록 정보=======")
            print(data_dict)
            print("======end API Contents 등록 정보=======")
            user = User.objects.get(id=user_id)
            category_id = data_dict.get('category_id')
            category = Categories.objects.get(id=category_id)
            # apicontent =  Contents(**body, added_by=user)
            apicontent =  Contents()
            apicontent.api_name = data_dict.get('api_name')
            apicontent.api_desc = data_dict.get('api_desc')
            apicontent.api_key = data_dict.get('api_key')
            apicontent.api_endpoint = data_dict.get('api_endpoint')
            apicontent.api_ref1 = data_dict.get('api_ref1')            
            apicontent.api_ref2 = data_dict.get('api_ref2')            
            apicontent.api_ref3 = data_dict.get('api_ref3')            
            apicontent.api_ref4 = data_dict.get('api_ref4')            
            apicontent.api_ref5 = data_dict.get('api_ref5')            
            apicontent.api_data_format = data_dict.get('api_data_format')            
            apicontent.updated  = datetime.datetime.utcnow          
            apicontent.added_by = user
            apicontent.category = category
            apicontent.seq = Contents.objects.count() + 1
            apicontent.save()
            user.update(push__contents=apicontent)
            user.save()
            category.update(push__contents=apicontent)
            category.save()
            print("API Contents 등록 성공 ...")
            return { 'id': str(apicontent.id),
                     'api_name': apicontent.api_name,
                     'api_desc': apicontent.api_desc,
                     'api_key': apicontent.api_key,
                     'api_endpoint': apicontent.api_endpoint,
                     'api_ref1': apicontent.api_ref1,
                     'api_ref2': apicontent.api_ref2,
                     'api_ref3': apicontent.api_ref3,
                     'api_ref4': apicontent.api_ref4,
                     'api_ref5': apicontent.api_ref5,
                     'api_data_format': apicontent.api_data_format,
                     'category_id': str(category.id),
                     'seq': apicontent.seq
                    }, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise ContentsAlreadyExistsError
        except Exception as e:
            raise InternalServerError

@Contents_NS.route('/<id>')
@Contents_NS.doc(params={'id': 'An ID'})
class ContentsApi(Resource):
    @Contents_NS.response(202, 'Success', api_content_fields_with_id)
    @Contents_NS.response(500, 'Failed')
    @jwt_required()
    def put(self, id: str):
        print("API Contents 수정 시작 ...")
        try:
            user_id = get_jwt_identity()
            apicontent = Contents.objects.get(id=id, added_by=user_id)
            # body = request.get_json()
            # Contents.objects.get(id=id).update(**body)
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======API Contents 수정 정보=======")
            print(data_dict)
            print("======end API Contents 수정 정보=======")
            # apicontent.api_name = data_dict.get('api_name')
            # Category에서 기존 참조 content 삭제
            remove_content_from_category = Categories.objects(id=str(apicontent.category.id)).update_one(pull__contents=apicontent)
            # remove_content_from_category.save()

            # 새로운 Category 참조를 위해 정보 가져옴
            category_id = data_dict.get('category_id')
            category = Categories.objects.get(id=category_id)

            apicontent.api_desc = data_dict.get('api_desc')
            apicontent.api_key = data_dict.get('api_key')
            apicontent.api_endpoint = data_dict.get('api_endpoint')
            apicontent.api_ref1 = data_dict.get('api_ref1')            
            apicontent.api_ref2 = data_dict.get('api_ref2')            
            apicontent.api_ref3 = data_dict.get('api_ref3')            
            apicontent.api_ref4 = data_dict.get('api_ref4')            
            apicontent.api_ref5 = data_dict.get('api_ref5')            
            apicontent.api_data_format = data_dict.get('api_data_format')
            apicontent.category = category
            apicontent.updated  = datetime.datetime.utcnow          
            apicontent.save()

            # Category에서 새로운 참조 content 등록
            category.update(push__contents=apicontent)
            category.save()

            print("API Contents 수정 성공 ...")
            return { 'id': str(apicontent.id),
                     'api_name': apicontent.api_name,
                     'api_desc': apicontent.api_desc,
                     'api_key': apicontent.api_key,
                     'api_endpoint': apicontent.api_endpoint,
                     'api_ref1': apicontent.api_ref1,
                     'api_ref2': apicontent.api_ref2,
                     'api_ref3': apicontent.api_ref3,
                     'api_ref4': apicontent.api_ref4,
                     'api_ref5': apicontent.api_ref5,
                     'api_data_format': apicontent.api_data_format,
                     'category_id': str(category.id),
                     'seq': apicontent.seq
                    }, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingContentsError
        except Exception:
            raise InternalServerError       
    
    @Contents_NS.doc(responses={202: 'Success'})
    @Contents_NS.doc(responses={500: 'Failed'})
    @jwt_required()
    def delete(self, id: str):
        print("API Contents 삭제 시작 ...")
        try:
            user_id = get_jwt_identity()
            apicontent = Contents.objects.get(id=id, added_by=user_id)
            apicontent.delete()
            print("API Contents id={} 삭제 성공 ...".format(id))
            return '', 200
        except DoesNotExist:
            raise DeletingContentsError
        except Exception:
            raise InternalServerError

    @Contents_NS.response(200, 'Success', api_content_fields_with_id)
    @Contents_NS.response(500, 'Failed')
    def get(self, id: str):
        print("API Contents 조회 시작 ...")
        try:
            apicontent = Contents.objects.get(id=id).to_json()
            print("API Contents id={} 조회 성공 ...".format(id))
            return Response(apicontent, mimetype="application/json", status=200)
        except DoesNotExist:
            raise ContentsNotExistsError
        except Exception:
            raise InternalServerError
