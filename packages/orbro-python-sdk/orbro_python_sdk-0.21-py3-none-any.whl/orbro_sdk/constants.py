from enum import Enum
DEFAULT_TOKEN_EXPIRES_IN = 1800000  # 30min.
DEFAULT_ISSUER = 'meta-platform-connect'
DEFAULT_TIMEOUT = 120
CONNECT_APP_USER_AGENT = 'meta-platform-connect'
WEBHOOK_USER_AGENT = 'meta-platform-webhook'
CONNECT_APP_ISSUE_TOKEN_URL = '/api/v1/oauth/token'
CONNECT_APP_AUTH_URL = '/api/v1/connect-auth/token'
AUTH_URL = '/api/v1/auth'
OAUTH_URL = '/api/v1/oauth/token'
PLATFORM_TOKEN_EXPIRED_ERROR_CODE = 'TOKEN_EXPIRED'


class AppTypeEnum(str, Enum):
    FLASK = 'Flask'
    FAST_API = 'FastAPI'


class HostEnum(str, Enum):
    DEV = 'kongmeta.dev'
    STG = 'kongmeta.kr'
    PROD = 'orbro.io'
