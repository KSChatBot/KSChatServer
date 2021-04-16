from .api_content import API_Content_NS
from .auth import Authentication_NS
from .reset_password import Password_NS
from .weather import WeaherInfo_NS

def initialize_routes(api):
    api.add_namespace(API_Content_NS, '/api/contents')

    api.add_namespace(Authentication_NS, '/accounts')

    api.add_namespace(WeaherInfo_NS, '/api/weather')

    api.add_namespace(Password_NS, '/api/auth')
    # api.add_resource(ForgotPassword, '/api/auth/forgot')
    # api.add_resource(ResetPassword, '/api/auth/reset')
