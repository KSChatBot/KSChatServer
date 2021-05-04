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
            # Category Cognigy_Chatbot
            Contents(
                api_paths="", 
                api_name="조선내화동영상데모용", 
                api_desc="조선내화 Cognigy 챗봇 도입을 위한 UiPath 업무자동화 로봇 연계  챗봇 데모로 출장신청, 재경업무 리포트 출력, 기타업무지원으로 구성됨", 
                api_key="", 
                api_endpoint="https://endpoint-bot.ks-cognigy.com/7a1ce65085fbf8626677f58034dce31c871128acfdcdee04fe02c8820039a41d", 
                category=category4, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()

            Contents(
                api_paths="", 
                api_name="헬프데스크", 
                api_desc="Cognigy 챗봇 소개를 위한 IT HelpDesk Service를 위한 챗봇으로 노트북등 디바이스 고장접수와 시스템 접속 패스워드 재설정 기능 제공", 
                api_key="", 
                api_endpoint="https://endpoint-bot.ks-cognigy.com/50f1f11bc6a0cc0a52b0746e7c262cec63543d8e66e4d93864ef9aff99946529", 
                category=category4, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()

            Contents(
                api_paths="", 
                api_name="동네날씨", 
                api_desc="네이버 날씨를 이용하여 동네 날씨정보를 제공하기 위한 챗봇으로 현재 날씨 기온과 미세먼지 농도를 알려준다.", 
                api_key="", 
                api_endpoint="https://endpoint-bot.ks-cognigy.com/2de0420f58eccc3c61f93d2f8abbc63177b80d6c0946c42d16890f569095f4c3", 
                category=category4, 
                added_by=user, 
                updated=datetime.datetime.utcnow 
                
            ).save()
            print("Content 등록 성공....")

            return {'등록 사용자 email': user.email}, 200

        except Exception as e:
            print("예외처리발생:",e)
