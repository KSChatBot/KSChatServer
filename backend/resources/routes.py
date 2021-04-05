from .api_content import API_Content_NS
from .auth import Authentication_NS
from .reset_password import Password_NS

def initialize_routes(api):
    api.add_namespace(API_Content_NS, '/api/contents')

    api.add_namespace(Authentication_NS, '/api/auth')
    # api.add_resource(SignupApi, '/api/auth/signup')
    # api.add_resource(LoginApi, '/api/auth/login')

    api.add_namespace(Password_NS, '/api/auth')
    # api.add_resource(ForgotPassword, '/api/auth/forgot')
    # api.add_resource(ResetPassword, '/api/auth/reset')
