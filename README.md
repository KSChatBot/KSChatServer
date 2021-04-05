# KS Chat Server 개요
챗봇이 다양한 대화 주제에 잘 대응 할 수 있도록 컨텐츠를 제공하기 위하여 웹상의 각종 정보를 클롤링하고, 공공데이터 서비스, 백오피스 시스템 연계를 통해서 챗봇 대화 진행시 필요한 정보와 컨텐츠를 Rest API로 제공한다. 기술 스택은 DevOps를 실현하기 위해 Docker를 활용한 컨테이너 빌드 배포 기능 위에 사용자 인터페이스 부분인 프런트엔드는 React로 하고, 백엔드는 Python Flask와 MongoDB를 사용한다.

## Chat Server가 실행 되기 위한 환경(Prerequisites)

 1. Node.js를 Node Package Manager(npm)와 함께 설치되어 있어야 합니다.
 2. 최신 버전의 Docker가 자기가 사용하는 OS(Windows, Mac, Linux등)에 맞게 설치되어 있어야 합니다.
 3. Python 버전 3.x를 설치해야 하고 최신 버전이 좋으나 최소 3.5이상이 설치 되어야합니다.
 4. Chat Server의 설치 개발 테스트를 위한 프로젝트 디렉토리를 생성합니다(Ex: chatwebapp).
 5. 코드 편집기를 설치 합니다.(예: VS Code).

## Docker로 실행
 1. 도커이미지 보기
    ```
    $ docker images
    ```

 2. Building an image
    ```
    $ docker-compose build
    ```

 3. Running a container
    ```
    $ docker-compose up
    ```

 4. Stopping a container
    ```
    $ docker-compose down
    ```

 5. 도커이미지 삭제
    ```
    $ docker rmi $(docker images -a -q)
    ```

 6. 도커이미지 컨테이너 백그라운드로 올리기
    ```
    $ docker-compose up -d
    ```

 7. 도커이미지 컨테이너에 다시 올리기
    ```
    $ docker-compose up --build 
    ```
## MongoDB 설정
```$ docker-compose up``` 명령어 실행후 최초로 Docker Container가 실행 되었을 경우는 MongoDB 사용 환경 설정이 필요하다.
 1. 다른 명령어 입력창(CLI)을 열고 Docker Container의 몽고디비 접속
    ```
    $ docker exec -it mongo bash
    ```

 2. 몽고디비 어드민 접속 그리고 패스워드 넣어야함(docker-compose.yml의 MONGO_INITDB_ROOT_PASSWORD: "password")
    ```
    $ root@786b840a5df7:/# mongo -u admin -p
    ```

 3. 새로운 몽고 디비용 프롬프트에서 몽고디비 생성 사용
    ```
    $ use webapp
    ```

 4. 몽고디비 사용자 생성
    ```
    $ db.createUser({user: 'apiuser', pwd: 'apipassword', roles: [{role: 'readWrite', db: 'webapp'}]})
    ```

 ## 아래 내용을 참조하였습니다.

  1. [How to set up a React app with a Flask and MongoDB backend using Docker][1]
  2. [Flask Rest API - Zero to Yoda (7 Part Series)][2]
  3. [React Boilerplate - Email Sign Up with Verification, Authentication & Forgot Password][3]


[1]: https://medium.com/swlh/how-to-set-up-a-react-app-with-a-flask-and-mongodb-backend-using-docker-19b356180199
[2]: https://dev.to/paurakhsharma/flask-rest-api-part-0-setup-basic-crud-api-4650
[3]: https://jasonwatmore.com/post/2020/04/22/react-email-sign-up-with-verification-authentication-forgot-password#account-forgot-password-jsx