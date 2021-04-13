from flask import Response, request
from database.models import API_Content, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, API_ContentAlreadyExistsError, InternalServerError, \
UpdatingAPI_ContentError, DeletingAPI_ContentError, API_ContentNotExistsError

API_Content_NS = Namespace(
    name="API_Content",
    description="API_Content 리스트를 작성하기 위해 사용하는 API.",
)

api_content_fields = API_Content_NS.model('API_Content', {  # Model 객체 생성
    'api_name': fields.String(description='a API_Content', required=True, example="공공데이타날씨정보"),
    'api_desc': fields.String(description='The API_Content api_desc'),
    'api_key': fields.String(description='The API_Content api_key'),
    'api_endpoint': fields.String(description='The API_Content api_endpoint'),
    'api_data_format': fields.String(description='The API_Content api_data_format')
})

api_content_fields_with_id = API_Content_NS.inherit('API_Content With ID', api_content_fields, {
    'id': fields.Integer(description='a API_Content ID')
})

@API_Content_NS.route('')
class API_ContentsApi(Resource):
    @API_Content_NS.doc('list_api_contents')
    def get(self):
        query = API_Content.objects()
        apicontents = API_Content.objects().to_json()
        return Response(apicontents, mimetype="application/json", status=200)

    @jwt_required
    @API_Content_NS.expect(api_content_fields)
    @API_Content_NS.response(201, 'Success', api_content_fields_with_id)
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            apicontent =  API_Content(**body, added_by=user)
            apicontent.save()
            user.update(push__apicontents=apicontent)
            user.save()
            id = apicontent.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise API_ContentAlreadyExistsError
        except Exception as e:
            raise InternalServerError

@API_Content_NS.route('/<id>')
@API_Content_NS.doc(params={'id': 'An ID'})
class API_ContentApi(Resource):
    @jwt_required
    @API_Content_NS.response(202, 'Success', api_content_fields_with_id)
    @API_Content_NS.response(500, 'Failed')
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            apicontent = API_Content.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            API_Content.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingAPI_ContentError
        except Exception:
            raise InternalServerError       
    
    @jwt_required
    @API_Content_NS.doc(responses={202: 'Success'})
    @API_Content_NS.doc(responses={500: 'Failed'})
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            apicontent = API_Content.objects.get(id=id, added_by=user_id)
            apicontent.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingAPI_ContentError
        except Exception:
            raise InternalServerError

    @API_Content_NS.response(200, 'Success', api_content_fields_with_id)
    @API_Content_NS.response(500, 'Failed')
    def get(self, id):
        try:
            apicontents = API_Content.objects.get(id=id).to_json()
            return Response(apicontents, mimetype="application/json", status=200)
        except DoesNotExist:
            raise API_ContentNotExistsError
        except Exception:
            raise InternalServerError
