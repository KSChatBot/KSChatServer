from flask import Response, request, json, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from database.models import API_Content, User
from flask_restx import Resource, Namespace, fields
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, API_ContentAlreadyExistsError, InternalServerError, \
UpdatingAPI_ContentError, DeletingAPI_ContentError, API_ContentNotExistsError
import datetime

API_Content_NS = Namespace(
    name="API_Content",
    description="API_Content 리스트를 작성하기 위해 사용하는 API.",
)

api_content_fields = API_Content_NS.model('API_Content', {  # Model 객체 생성
    'api_name': fields.String(description='a API_Content', required=True, example="날씨정보"),
    'api_desc': fields.String(description='The API_Content api_desc', example="공공데이타날씨정보"),
    'api_key': fields.String(description='The API_Content api_key'),
    'api_endpoint': fields.String(description='The API_Content api_endpoint'),
    'api_data_format': fields.String(description='The API_Content api_data_format') 
})

api_content_fields_with_id = API_Content_NS.inherit('API_Content With ID', api_content_fields, {
    'id': fields.String(description='a API_Content ID')
})

@API_Content_NS.route('')
class API_ContentsApi(Resource):
    @API_Content_NS.doc('list_api_contents')
    def get(self):
        query = API_Content.objects()
        apicontents = API_Content.objects().to_json()
        print("API Contents 조회 성공 ...")
        return Response(apicontents, mimetype="application/json", status=200)

    @API_Content_NS.expect(api_content_fields)
    @API_Content_NS.response(201, 'Success', api_content_fields_with_id)
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
            # apicontent =  API_Content(**body, added_by=user)
            apicontent =  API_Content()
            apicontent.api_name = data_dict.get('api_name')
            apicontent.api_desc = data_dict.get('api_desc')
            apicontent.api_key = data_dict.get('api_key')
            apicontent.api_endpoint = data_dict.get('api_endpoint')
            apicontent.api_data_format = data_dict.get('api_data_format')            
            apicontent.updated  = datetime.datetime.utcnow          
            apicontent.added_by = user
            apicontent.seq = API_Content.objects.count() + 1
            apicontent.save()
            user.update(push__api_contents=apicontent)
            user.save()
            print("API Contents 등록 성공 ...")
            return { 'id': str(apicontent.id),
                     'api_name': apicontent.api_name,
                     'api_desc': apicontent.api_desc,
                     'api_key': apicontent.api_key,
                     'api_endpoint': apicontent.api_endpoint,
                     'api_data_format': apicontent.api_data_format,
                     'seq': apicontent.seq
                    }, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise API_ContentAlreadyExistsError
        except Exception as e:
            raise InternalServerError

@API_Content_NS.route('/<id>')
@API_Content_NS.doc(params={'id': 'An ID'})
class API_ContentApi(Resource):
    @API_Content_NS.response(202, 'Success', api_content_fields_with_id)
    @API_Content_NS.response(500, 'Failed')
    @jwt_required()
    def put(self, id: str):
        print("API Contents 수정 시작 ...")
        try:
            user_id = get_jwt_identity()
            apicontent = API_Content.objects.get(id=id, added_by=user_id)
            # body = request.get_json()
            # API_Content.objects.get(id=id).update(**body)
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======API Contents 수정 정보=======")
            print(data_dict)
            print("======end API Contents 수정 정보=======")
            apicontent.api_name = data_dict.get('api_name')
            apicontent.api_desc = data_dict.get('api_desc')
            apicontent.api_key = data_dict.get('api_key')
            apicontent.api_endpoint = data_dict.get('api_endpoint')
            apicontent.api_data_format = data_dict.get('api_data_format')
            apicontent.updated  = datetime.datetime.utcnow          
            apicontent.save()
            print("API Contents 수정 성공 ...")
            return { 'id': str(apicontent.id),
                     'api_name': apicontent.api_name,
                     'api_desc': apicontent.api_desc,
                     'api_key': apicontent.api_key,
                     'api_endpoint': apicontent.api_endpoint,
                     'api_data_format': apicontent.api_data_format,
                     'seq': apicontent.seq
                    }, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingAPI_ContentError
        except Exception:
            raise InternalServerError       
    
    @API_Content_NS.doc(responses={202: 'Success'})
    @API_Content_NS.doc(responses={500: 'Failed'})
    @jwt_required()
    def delete(self, id: str):
        print("API Contents 삭제 시작 ...")
        try:
            user_id = get_jwt_identity()
            apicontent = API_Content.objects.get(id=id, added_by=user_id)
            apicontent.delete()
            print("API Contents id={} 삭제 성공 ...".format(id))
            return '', 200
        except DoesNotExist:
            raise DeletingAPI_ContentError
        except Exception:
            raise InternalServerError

    @API_Content_NS.response(200, 'Success', api_content_fields_with_id)
    @API_Content_NS.response(500, 'Failed')
    def get(self, id: str):
        print("API Contents 조회 시작 ...")
        try:
            apicontent = API_Content.objects.get(id=id).to_json()
            print("API Contents id={} 조회 성공 ...".format(id))
            return Response(apicontent, mimetype="application/json", status=200)
        except DoesNotExist:
            raise API_ContentNotExistsError
        except Exception:
            raise InternalServerError
