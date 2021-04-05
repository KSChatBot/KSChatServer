# React Boilerplate 앱 개요
React Boilerplate 앱은 기본적으로 가짜 백엔드로 실행되어 실제 백엔드 API (백엔드없는)없이 브라우저에서 완전히 실행되도록하고, 실제 백엔드 API로 전환하려면 앱 구동을 위한 진입점 파일(/src/index.jsx)에서 몇 줄의 코드 만 제거하면됩니다. Python Flask + MongoDB와 연결할 수 있습니다.

기본적으로 애플리케이션에 등록 된 사용자가 없습니다. 로그인하려면 먼저 계정을 등록하고 확인해야합니다. 가짜 백엔드는 실제 이메일을 보낼 수 없기 때문에 화면에 "이메일"메시지를 표시하므로 등록 후 방금 등록한 계정을 확인하는 링크가있는 "확인 이메일"이 표시됩니다. 링크를 클릭하여 계정을 확인하고에 로그인합니다.

등록 된 첫 번째 사용자는 Admin역할에 할당 되고 후속 사용자는 일반 User역할에 할당됩니다 . 관리자는 관리자 섹션에 액세스하여 모든 사용자를 관리 할 수 ​​있지만 일반 사용자는 자신의 프로필(profile)만 업데이트 할 수 있습니다.

## refresh tokens을 사용한 JWT 인증
인증은 JWT 액세스 토큰(WT access token) 및 새로 고침 토큰(refresh token)을 사용하여 구현됩니다. 인증에 성공하면 api(또는 가짜 백엔드)는 15분 후에 만료되는 짧은 라이브 JWT 액세스 토큰과 쿠키에서 7일 후에 만료되는 새로 고침 토큰을 반환합니다. JWT는 api의 보안 경로에 액세스하기 위해 사용되며, 새로 고침 토큰은 JWT 액세스 토큰이 만료될 때(또는 직전에) Ract 앱이 타이머를 시작하여 JWT 토큰이 만료되기 1분 전에 업데이트되어 사용자가 로그인할 수 있도록 합니다.

## 로컬에서 React Boilerplate App 실행
 1. https://nodejs.org에서 NodeJS 및 NPM 설치
 2. https://github.com/cornflourblue/react-signup-verification-boilerplate에서 프로젝트 소스 코드를 다운로드하거나 복제합니다.
 3. 프로젝트 루트 폴더(패키지)의 명령줄에서 npm 설치를 실행하여 필요한 모든 npm 패키지를 설치합니다.json이 있습니다.)
 4. 프로젝트 루트 폴더의 명령줄에서 npm start를 실행하여 응용 프로그램을 시작하면 응용 프로그램을 표시하는 브라우저가 시작됩니다.

 ## 아래 내용을 참조하였습니다.

React - Email Sign Up with Verification, Authentication & Forgot Password

For documentation and a live demo see https://jasonwatmore.com/post/2020/04/22/react-email-sign-up-with-verification-authentication-forgot-password
