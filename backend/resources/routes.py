from .api_content import Contents_NS
from .auth import Authentication_NS
from .reset_password import Password_NS
from .weather import WeatherInfo_NS
from .category import Categories_NS
from .setup_db import SetUpDB_NS
from .uipath_orchestrator import UiPathOrchestrator_NS

def initialize_routes(api):
    api.add_namespace(SetUpDB_NS, '/api/db')
    api.add_namespace(Categories_NS, '/api/categories')
    api.add_namespace(Contents_NS, '/api/contents')

    api.add_namespace(Authentication_NS, '/accounts')

    api.add_namespace(UiPathOrchestrator_NS, '/api/uipath')
    api.add_namespace(WeatherInfo_NS, '/api/weather')

    api.add_namespace(Password_NS, '/api/auth')
    # api.add_resource(ForgotPassword, '/api/auth/forgot')
    # api.add_resource(ResetPassword, '/api/auth/reset')
