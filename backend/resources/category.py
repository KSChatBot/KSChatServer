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
from resources.errors import SchemaValidationError, CategoriesAlreadyExistsError, InternalServerError, \
UpdatingCategoriesError, DeletingCategoriesError, CategoriesNotExistsError
import datetime

Categories_NS = Namespace(
    name="Categories",
    description="Categories 리스트를 작성하기 위해 사용하는 API.",
)

api_content_fields = Categories_NS.model('Categories', {  # Model 객체 생성
    'name': fields.String(description='a Categories', required=True, example="API분류명으로 API정보, UiPath_Orchestrator, ChatBot정보"),
    'desc': fields.String(description='The Categories description')
})

api_content_fields_with_id = Categories_NS.inherit('Categories With ID', api_content_fields, {
    'id': fields.String(description='a Categories ID')
})
