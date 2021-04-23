from .api_content import Contents_NS
from .auth import Authentication_NS
from .reset_password import Password_NS
from .weather import WeatherInfo_NS

def initialize_routes(api):
    api.add_namespace(Contents_NS, '/api/contents')

    api.add_namespace(Authentication_NS, '/accounts')

    api.add_namespace(WeatherInfo_NS, '/api/weather')

    api.add_namespace(Password_NS, '/api/auth')
    # api.add_resource(ForgotPassword, '/api/auth/forgot')
    # api.add_resource(ResetPassword, '/api/auth/reset')
