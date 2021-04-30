import requests
import json


def getUserToken(URL, tenancyName, usernameOrEmailAddress, password):
    # data = requests.post(url, json=json.loads(user_data), verify=False)
    # authentication_data = json.loads(data.text)
    # token = "Bearer " + str(authentication_data["result"])
    data = {
        "tenancyName": tenancyName,
        "usernameOrEmailAddress": usernameOrEmailAddress,
        "password": password

    }
    sess = requests.Session()
    data = requests.post(URL, json=data, verify=False)
    if(data.status_code == 200):
        authentication_data = json.loads(data.text)
        token = "Bearer " + str(authentication_data["result"])
    else:
        token = "Bearer "

    return token


def getProcessID(process_name, token):
    process_data = requests.get(f"https://koreascoring.iptime.org/odata/Releases?$filter=ProcessKey+eq%20'{process_name}'",
                                headers={"Authorization": token}, verify=False)
    process_json = json.loads(process_data.text)
    # print(json.dumps(process_json, indent=2))
    process_ID = process_json["value"][0]["Key"]
    return process_ID


def getRobotID(robotName, token):
    robot_name = requests.get(f"https://koreascoring.iptime.org/odata/Robots?$filter=Name%20eq%20'{robotName}'",
                              headers={"Authorization": token}, verify=False)
    robot_json_obj = json.loads(robot_name.text)
    robot_ID = robot_json_obj["value"][0]["Id"]
    return robot_ID


def runJob(process_ID, robot_ID, token):
    start_job_json = """{ "startInfo":
       { "ReleaseKey": \"""" + process_ID + """\",
         "Strategy": "Specific",
         "RobotIds": [ """ + str(robot_ID) + """ ],
         "Source": "Manual",
         "InputArguments": "{'in_Arg1':'Aloha'}"        
       } 
    }"""  # InputArguments should be left {} or not included if workflow does not accept any input
    start_job_data = requests.post("https://koreascoring.iptime.org/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs",
                                   json=json.loads(start_job_json), headers={"Authorization": token}, verify=False)
    return start_job_data



if __name__ == "__main__":
    # ---Steps to run a JOB---

    # ---Step 1. - Get the Orchestrator TOKEN---
    # Authentication Data
    
    tenant_name = str(input("Please enter the Tenant Name: \n"))
    owner_name = str(input("Please enter the User Name: \n"))
    tenant_email  = str(input("Please enter the Tenant Email: \n"))
    tenant_password  = str(input("Please enter the Tenant Password: \n"))
    url = "https://koreascoring.iptime.org/api/Account/Authenticate"
    user_data = """{
        	"tenancyName": \"""" + tenant_name + """\",
        	"usernameOrEmailAddress": \"""" + tenant_email +"""\",
        	"password": \""""+ tenant_password + """\"
        }"""
    token = getUserToken(url, tenant_name, owner_name, tenant_password)
    print("Token = " + token)

    # ---Step 2. - Get PROCSS_ID of process you want to run---
    process_name = str(input("Please enter the Process Name: \n"))
    process_ID = getProcessID(process_name, token)
    print(f"Process ID = {process_ID}")

    # ---Step 3. - Get the ROBOT_ID of robot you want to run process on---
    robot_name = str(input("Please enter the Robot Name: \n"))
    robot_ID = getRobotID(robot_name, token)
    print(f"Robot ID = {robot_ID}")

    # ---Step 4. - START_Job---
    start_job_data = runJob(process_ID, robot_ID, token)
    print("Job Status = " + str(start_job_data))