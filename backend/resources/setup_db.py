from flask import Response, request, json, jsonify
from flask_restx import Resource, Namespace, fields
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, InvalidQueryError
from mongoengine import connect
from database.models import User, Categories, Contents
import json

SetUpDB_NS = Namespace(
    name="Database Set up",
    description="웹 어플리케이션을 위한 초기 데이터베이스 설정",
)

@SetUpDB_NS.route('/setup')
class SetupDBApi(Resource):
    def post(self):
        try:
# {'email': 'admin@koreascoring.com', 'password': '123456', 'role':'Admin', 'title': 'Mr', 'firstName': 'System', 'lastName': 'Admin', 'acceptTerms': True}
            
            print("기존 사용자 전체 삭제....")
            User.objects().delete()
            print("기존 사용자 전체 삭제 성공....")

            print("기존 Category 전체 삭제....")
            Categories.objects().delete()
            print("기존 Category 전체 삭제 성공....")

            print("사용자 등록....")
            adminUser = User(
                email="admin@koreascoring.com",
                password="123456",
                role="Admin",
                title="Mr",
                firstName="System",
                lastName="Admin",
                acceptTerms=True
            )
            adminUser.hash_password()
            user = adminUser.save()
            print("사용자 등록 성공....")

            print("Category 등록....")
            category1 = Categories(name="일반", desc="챗봇에서 사용할 일반 정보제공 API").save()
            category2 = Categories(name="RPA_UiPah_OnPremise", desc="UiPath On Premise Orchestrator API").save()
            category3 = Categories(name="RPA_UiPah_Cloud", desc="UiPath Cloud Orchestrator API").save()
            category4 = Categories(name="Cognigy_Chatbot", desc="Cognigy로 만든 챗봇 API").save()

            print("Category 등록 성공....")

            print("Content 등록....")
            # Category 일반
            Contents(
                api_paths="/api/weather/get_naver", 
                api_name="네이버날씨", 
                api_desc="네이버에서 날씨 정보를 가져와서 제공하는 API", 
                api_key="", 
                api_endpoint="https://search.naver.com/search.naver?", 
                category=category1, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()
            Contents(
                api_paths="/api/weather/get_public_data", 
                api_name="날씨동네예보조회", 
                api_desc="공공데이터 동네예보조회 날씨 정보를 가져와서 제공하는 API", 
                api_key="gC8RUN3kxgc5v1ZNPvEYW%2FspE4YwHYOn7VWWlIQGfGw2fNVEBCrzvE8cHUFEZpxk6jHmkvwHK9RuL2EjzNz4WQ%3D%3D", 
                api_endpoint="http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?", 
                category=category1, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()

            # Category RPA_UiPah_OnPremise
            Contents(
                api_paths="/api/uipath/get_releases", 
                api_name="UiPath_Orchestrator_Releases", 
                api_desc="UiPath Orchestrator에 등록된 전체 프로로세스의 Key, ProcessKey(프로세스명), InputArguments로 구성된 목록을 가져오는 API", 
                api_key="", 
                api_endpoint="https://koreascoring.iptime.org", 
                api_ref1="Default", 
                api_ref2="admin", 
                api_ref3="1q2w3e4r!", 
                category=category2, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()
            Contents(
                api_paths="/api/uipath/get_robots", 
                api_name="UiPath_Orchestrator_Robots", 
                api_desc="UiPath Orchestrator에 등록된 전체 로봇의 ID, Name으로 구성된 목록을 가져오는 API", 
                api_key="", 
                api_endpoint="https://koreascoring.iptime.org", 
                api_ref1="Default", 
                api_ref2="admin", 
                api_ref3="1q2w3e4r!", 
                category=category2, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()
            Contents(
                api_paths="/api/uipath/get_process_id", 
                api_name="UiPath_Orchestrator_process_id", 
                api_desc="UiPath Orchestrator에서 프로세스명으로 프로세스의 ID를 가져오는 API", 
                api_key="", 
                api_endpoint="https://koreascoring.iptime.org", 
                api_ref1="Default", 
                api_ref2="admin", 
                api_ref3="1q2w3e4r!", 
                category=category2, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()
            Contents(
                api_paths="/api/uipath/get_robot_id", 
                api_name="UiPath_Orchestrator_robot_id", 
                api_desc="UiPath Orchestrator에서 로봇명으로 로봇의 ID를 가져오는 API", 
                api_key="", 
                api_endpoint="https://koreascoring.iptime.org", 
                api_ref1="Default", 
                api_ref2="admin", 
                api_ref3="1q2w3e4r!", 
                category=category2, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()
            Contents(
                api_paths="/api/uipath/runjob", 
                api_name="UiPath_Orchestrator_runjob", 
                api_desc="UiPath Orchestrator에 등록된 프로세스를 로봇이 실행하도록 프로세스 ID, 로봇 ID, 입력 변수명과 값을 주고 작업을 실행하는 API", 
                api_key="", 
                api_endpoint="https://koreascoring.iptime.org", 
                api_ref1="Default", 
                api_ref2="admin", 
                api_ref3="1q2w3e4r!", 
                category=category2, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()

            print("Content 등록 성공....")

            return {'등록 사용자 email': user.email}, 200

        except Exception as e:
            print("예외처리발생:",e)
