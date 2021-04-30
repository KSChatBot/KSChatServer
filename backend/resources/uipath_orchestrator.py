import requests as req
import json
import pandas as pd
import datetime
from flask import Response, request, json, jsonify
from flask_restx import Resource, Namespace, fields
from database.models import Contents, User
import services.weather_info as wf

UiPathOrchestrator_NS = Namespace(
    name="UiPath Orchestrator REST API",
    description="UiPath Orchestrator에서 관리되는 Process, Robot, Job에 대한 API.",
)

releases_fields = UiPathOrchestrator_NS.model('OnPremiseReleases', {  # Model 객체 생성
    'api_name': fields.String(description='a Contents', required=True, example="UiPath_Orchestrator_Releases")
})
robots_fields = UiPathOrchestrator_NS.model('OnPremiseRobots', {
    'api_name': fields.String(description='a Contents', required=True, example="UiPath_Orchestrator_Releases")
 })
get_process_id_fields = UiPathOrchestrator_NS.model('OnPremiseProcessID', {
    'api_name': fields.String(description='a Contents', required=True, example="UiPath_Orchestrator_Releases"),
    'process_name': fields.String(description='a Process Name in Orchestrator', required=True)
})
get_robot_id_fields = UiPathOrchestrator_NS.model('OnPremiseRobotID', {
    'api_name': fields.String(description='a Contents', required=True, example="UiPath_Orchestrator_Releases"),
    'robot_name': fields.String(description='a Robot Name in Orchestrator', required=True)
})
rubjob_fields = UiPathOrchestrator_NS.model('OnPremiseRunJob', {
    'api_name': fields.String(description='a Contents', required=True, example="UiPath_Orchestrator_Releases"),
    'process_id': fields.String(description='a Process ID in Orchestrator', required=True),
    'robot_id': fields.String(description='a Robot ID in Orchestrator', required=True),
    'InputArguments': fields.String(description='입력변수명, 값의 쌍으로 구성', example="{'in_Arg1':'100'}")
})

# UiPath Orchestrator에 로그인 정보를 주고 토큰을 받아온다.
def getUserToken(URL, tenancyName, usernameOrEmailAddress, password):
        try:
            user_data = {
                "tenancyName": tenancyName,
                "usernameOrEmailAddress": usernameOrEmailAddress,
                "password": password
            }
            print("URL :",URL)
            print("user_data :",user_data)
            # headers={'Content-type':'application/json', 'Accept':'application/json'}
            data = req.post(URL, json=user_data, verify=False)
            print("data.status_code :",data.status_code)
            if(data.status_code == 200):
                authentication_data = json.loads(data.text)
                token = "Bearer " + str(authentication_data["result"])
            else:
                token = "Bearer "

            return token

        except Exception as e:
            print("getUserToken Exception error! ==> ",e)

@UiPathOrchestrator_NS.route('/get_releases')
class UiPathOrchestratorReleasesAPI(Resource):
    @UiPathOrchestrator_NS.expect(releases_fields)
    def post(self):
        """UiPath Orchestrator에 등록된 전체 프로로세스의 Key, ProcessKey(프로세스명), InputArguments로 구성된 목록을 가져옵니다."""
        print("프로세스 목록 가져오기 ...")
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======프로세스 목록 정보=======")
            print(data_dict)
            print("======end 프로세스 목록 정보=======")
            api_name = data_dict.get('api_name')
            apicontent = Contents.objects.get(api_name=api_name)

            # 인증 토큰 받는 url
            url = apicontent.api_endpoint + "/api/Account/Authenticate"
            token = getUserToken(url, apicontent.api_ref1, apicontent.api_ref2, apicontent.api_ref3 )
            # print("인증 토큰 받은 토큰 :",token)

            process_data = req.get(apicontent.api_endpoint + "/odata/Releases", headers={"Authorization": token}, verify=False)
            process_json = json.loads(process_data.text)
            # print("process_json :",process_json)

            table_data = pd.DataFrame(process_json['value'])

            # 출력 결과를 JSON으로 가공 출력
            result = json.loads(json.dumps(list(table_data[['Key','ProcessKey','InputArguments']].T.to_dict().values())))
            # print("result :",result)


            print('프로세스 목록 종료...')
            return result, 200

        except Exception as e:
            print("get_releases Exception error! ==> ",e)

@UiPathOrchestrator_NS.route('/get_robots')
class UiPathOrchestratorRobotListAPI(Resource):
    @UiPathOrchestrator_NS.expect(robots_fields)
    def post(self):
        """UiPath Orchestrator에 등록된 전체 로봇의 ID, Name으로 구성된 목록을 가져옵니다."""
        print("로봇 목록 가져오기 ...")
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======로봇 목록 정보=======")
            print(data_dict)
            print("======end 로봇 목록 정보=======")
            api_name = data_dict.get('api_name')
            apicontent = Contents.objects.get(api_name=api_name)

            # 인증 토큰 받는 url
            url = apicontent.api_endpoint + "/api/Account/Authenticate"
            # print("인증 토큰 받는 url :",url)
            token = getUserToken(url, apicontent.api_ref1, apicontent.api_ref2, apicontent.api_ref3 )
            # print("인증 토큰 받은 토큰 :",token)

            robots_data = req.get(apicontent.api_endpoint + "/odata/Robots", headers={"Authorization": token}, verify=False)
            robots_json = json.loads(robots_data.text)
            # print("robots_json :",robots_json)

            table_data = pd.DataFrame(robots_json['value'])

            # 출력 결과를 JSON으로 가공 출력
            result = json.loads(json.dumps(list(table_data[['Name','Id']].T.to_dict().values())))
            print("result :",result)


            print('로봇 목록 종료...')
            return result, 200

        except Exception as e:
            print("get_releases Exception error! ==> ",e)

@UiPathOrchestrator_NS.route('/get_process_id')
class UiPathOrchestratorProcessAPI(Resource):
    @UiPathOrchestrator_NS.expect(get_process_id_fields)
    def post(self):
        """UiPath Orchestrator에서 프로세스명으로 프로세스의 ID를 가져옵니다."""
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======프로세스 정보=======")
            print(data_dict)
            print("======end 프로세스 정보=======")
            api_name = data_dict.get('api_name')
            process_name = data_dict.get('process_name')

            apicontent = Contents.objects.get(api_name=api_name)

            # 인증 토큰 받는 url
            url = apicontent.api_endpoint + "/api/Account/Authenticate"
            # print("인증 토큰 받는 url :",url)
            token = getUserToken(url, apicontent.api_ref1, apicontent.api_ref2, apicontent.api_ref3 )
            # print("인증 토큰 받은 토큰 :",token)
            process_data = req.get(apicontent.api_endpoint + "/odata/Releases?$filter=ProcessKey+eq%20" + process_name,
                                        headers={"Authorization": token}, verify=False)
            process_json = json.loads(process_data.text)
            # print(json.dumps(process_json, indent=2))
            process_ID = process_json["value"][0]["Key"]

            print('프로세스 ID 가져오기...')
            return { 'process_id': process_ID
            }, 200

        except Exception as e:
            print("get_process_id Exception error! ==> ",e)

@UiPathOrchestrator_NS.route('/get_robot_id')
class UiPathOrchestratorRobotsAPI(Resource):
    @UiPathOrchestrator_NS.expect(get_robot_id_fields)
    def post(self):
        """UiPath Orchestrator에서 로봇명으로 로봇의 ID를 가져옵니다."""
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======로봇 ID 정보=======")
            print(data_dict)
            print("======end 로봇 ID 정보=======")
            api_name = data_dict.get('api_name')
            robot_name = data_dict.get('robot_name')

            apicontent = Contents.objects.get(api_name=api_name)

            # 인증 토큰 받는 url
            url = apicontent.api_endpoint + "/api/Account/Authenticate"
            # print("인증 토큰 받는 url :",url)
            token = getUserToken(url, apicontent.api_ref1, apicontent.api_ref2, apicontent.api_ref3 )
            # print("인증 토큰 받은 토큰 :",token)
            robot_data = req.get(apicontent.api_endpoint + "/odata/Robots?$filter=Name%20eq%20" + robot_name,
                                        headers={"Authorization": token}, verify=False)
            robot_json = json.loads(robot_data.text)
            # print(json.dumps(process_json, indent=2))
            robot_ID = robot_json["value"][0]["Key"]

            print('로봇 ID 가져오기...')
            return { 'robot_id': robot_ID
            }, 200

        except Exception as e:
            print("get_robot_id Exception error! ==> ",e)

@UiPathOrchestrator_NS.route('/runjob')
class UiPathOrchestratorRunJobAPI(Resource):
    @UiPathOrchestrator_NS.expect(rubjob_fields)
    def post(self):
        """UiPath Orchestrator에 등록된 프로세스를 로봇이 실행하도록 프로세스 ID, 로봇 ID, 입력 변수명과 값을 주고 작업을 실행합니다."""
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("====== RunJob 정보=======")
            print(data_dict)
            print("======end RunJob 정보=======")
            api_name = data_dict.get('api_name')
            process_id = data_dict.get('process_id')
            robot_id = data_dict.get('robot_id')
            InputArguments = data_dict.get('InputArguments')

            apicontent = Contents.objects.get(api_name=api_name)

            # 인증 토큰 받는 url
            url = apicontent.api_endpoint + "/api/Account/Authenticate"
            # print("인증 토큰 받는 url :",url)
            token = getUserToken(url, apicontent.api_ref1, apicontent.api_ref2, apicontent.api_ref3 )
            # print("인증 받은 토큰 :",token)
            start_job_json = """{ "startInfo":
                                    { "ReleaseKey": \"""" + process_id + """\",
                                        "Strategy": "Specific",
                                        "RobotIds": [ """ + robot_id + """ ],
                                          "Source": "Manual",
                                  "InputArguments": \"""" + InputArguments + """\" 
                                }
          }"""  # InputArguments should be left {} or not included if workflow does not accept any input
            data = req.post(apicontent.api_endpoint + "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs",
                                    json=json.loads(start_job_json), headers={"Authorization": token}, verify=False)

            print('프로세스 로봇 실행하기...')
            return {'result code': data.status_code}, 200

        except Exception as e:
            print("runjob Exception error! ==> ",e)




