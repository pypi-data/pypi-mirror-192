import inspect, json, os, logging
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declarative_base
from .exceptions import InvalidAppClassException, InvalidAppDescriptorException
from .models import ConnectAppClientInfoMixin
from .datastore import RedisTokenDataStore, DictTokenDataStore, ClientInfoDataStore
from .constants import AppTypeEnum, HostEnum
from .util import TokenUtil


class OrbroConnect:
    token_store_dep = None
    client_info_store_dep = None
    token_util: TokenUtil = None
    engine = None
    host: str = None
    open_api_token = None

    def __init__(self, app, client_id: str = None, client_secret: str = None,
                 client_info_model=None, db_session_maker=None, redis=None,
                 descriptor_path='./connect.json', descriptor_url='/connect.json', env=None, open_api_token=None):
        app_type = type(app)
        if inspect.isclass(app_type):
            self._app_class_name = app_type.__name__
            self.app = app
        else:
            raise InvalidAppClassException(app)

        self.client_id = client_id
        self.client_secret = client_secret
        OrbroConnect.open_api_token = self.open_api_token = open_api_token
        self.model = client_info_model
        self._logger = logging.getLogger(__name__)
        self._init_app_env(env)
        self._init_app_descriptor(descriptor_path)
        self.descriptor_url = descriptor_url
        self._init_token_util()

        if db_session_maker:
            self.db = db_session_maker
        else:
            if self.env is not 'dev':
                self._logger.warning('SQLAlchemy sessionmaker is None. '
                                     'Connect app client information is managed in SQLite memory. '
                                     'If your app''s environment is not a development environment, '
                                     'the use of a persistent database is recommended.')
            self._init_dev_sqlite()

        self.client_info_datastore = ClientInfoDataStore(self.db, self.model)

        if redis:
            self.redis = redis
            self.token_store = RedisTokenDataStore(self.redis)
        else:
            self.redis = None
            if self.env is not 'dev':
                self._logger.warning('Redis is None. '
                                     'Connect app token information is managed in Python Dictionary. '
                                     'If your app''s environment is not a development environment, '
                                     'the use of a Redis is recommended.')
            self.token_store = DictTokenDataStore()
        if self.is_fastapi():
            self._logger.info('this is FastAPI Application. Initialize middleware and routers.')
            self._init_middleware()
            self._init_router()
        else:
            self._logger.error('SDK doesn''t support Flask yet...')

    def is_fastapi(self):
        return True if self._app_class_name is AppTypeEnum.FAST_API.value else False

    def is_flask(self):
        return True if self._app_class_name is AppTypeEnum.FLASK.value else False

    def _init_dev_sqlite(self):
        engine = create_engine('sqlite://', echo=True,
                               connect_args={"check_same_thread": False}, poolclass=StaticPool)
        if self.model is None:
            Base = declarative_base()
            self._logger.warning('The client information model does not exist. '
                                 'The SDK creates its own client information model.')

            class ConnectAppClientInfo(Base, ConnectAppClientInfoMixin):
                organization_id = Column(String(255), nullable=False)
                installed_user_id = Column(String(255))
                pass

            self.model = ConnectAppClientInfo
            Base.metadata.create_all(bind=engine)

        OrbroConnect.engine = engine
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def _init_app_env(self, env):
        """
             현재 실행된 Application의 환경(env) 체크
        """
        if env is None:
            app_class_name = self._app_class_name
            env = self.env = os.environ.get('SERVICE_ENV', None) or os.environ.get('ENV', None)
            if env is None:
                if app_class_name is AppTypeEnum.FAST_API.value:
                    self.env = 'dev'
                elif app_class_name is AppTypeEnum.FLASK.value:
                    self.env = self._app.config['ENV'] or 'dev'
        else:
            self.env = env

        OrbroConnect.host = HostEnum[self.env.upper()].value

    def get_app_class_name(self):
        """
            현재 실행된 Application의 Class 이름 리턴
        """
        return self._app_class_name

    def get_app_env(self):
        """
             현재 실행된 Application의 환경 리턴
        """
        return self.env

    def validate_app_descriptor(self, descriptor):
        """
            App Descriptor(e.g : connect.json) 정보 검증/유효성 체크
        """
        # TODO : 추후 pydantic Model이 반영된 models.descriptor로 유효성 체크 대체하도록 변경 필요.
        app_id = descriptor.get('id')
        if app_id is None:
            raise InvalidAppDescriptorException('app id is NULL')

        lifecycle = descriptor.get('lifecycle')
        if lifecycle:
            lifecycle_installed_url = lifecycle.get('installed')
            lifecycle_uninstalled_url = lifecycle.get('uninstalled')
            if not (lifecycle_installed_url and lifecycle_uninstalled_url):
                self._print_lifecycle_warning()
        else:
            self._print_lifecycle_warning()

    def _init_app_descriptor(self, descriptor_path):
        """
            App Descriptor(e.g : connect.json) 파일 로딩
        """
        try:
            with open(descriptor_path, 'r') as file:
                data = json.load(file)
        except Exception as e:
            raise InvalidAppDescriptorException(str(e))

        self.descriptor_path = descriptor_path
        self.validate_app_descriptor(data)
        self.descriptor = data
        return self.descriptor

    def _init_token_util(self):
        token_util = TokenUtil(self.client_id, self.client_secret, OrbroConnect.host)
        OrbroConnect.token_util = token_util
        return token_util

    def _print_lifecycle_warning(self):
        self._logger.warning('Lifecycle does not exist in app descriptor. '
                             'Organization information may not be dynamically '
                             'applied in a non-Web environment. (e.g : Mobile)')

    def _init_middleware(self):
        # Global DB 접근 Middlware이나 쓰이지 않음. (Deprecated)
        # from .fastapi.middleware.database import DBSessionMiddleware
        # self.app.add_middleware(DBSessionMiddleware, session=self.db)

        # Connect 앱 인증 Middleware 추가
        from .fastapi.middleware.auth import ConnectAppAuthMiddleware
        self.app.add_middleware(ConnectAppAuthMiddleware)
        self._logger.debug('ConnectAppAuthMiddleware has been added.')

    def _init_router(self):
        from fastapi import APIRouter, Depends
        from .fastapi.dependencies.database import ClientInfoStoreDep, DictTokenStoreDep, RedisTokenStoreDep

        if self.redis:
            self._logger.info('Create a token store with Redis.')
            OrbroConnect.token_store_dep = RedisTokenStoreDep(self.redis, self.token_store)
        else:
            self._logger.info('Create a token store with Python Dictionary.')
            OrbroConnect.token_store_dep = DictTokenStoreDep(self.token_store)

        OrbroConnect.client_info_store_dep = ClientInfoStoreDep(self.db, self.client_info_datastore)

        self.api_router = APIRouter(tags=['Connect App SDK'])
        lifecycle = self.descriptor.get('lifecycle')

        if lifecycle:
            from .fastapi.api_router.lifecycle import on_installed, on_uninstalled
            lifecycle_installed_url = lifecycle.get('installed')
            lifecycle_uninstalled_url = lifecycle.get('uninstalled')
            if lifecycle_installed_url:
                self.api_router.add_api_route(lifecycle_installed_url, on_installed, methods=['POST'])
                self._logger.debug('installed lifecycle route added. (url)'.format(url=lifecycle_installed_url))
            if lifecycle_uninstalled_url:
                self.api_router.add_api_route(lifecycle_uninstalled_url, on_uninstalled, methods=['POST'])
                self._logger.debug('uninstalled lifecycle route added. (url)'.format(url=lifecycle_uninstalled_url))

        # Connect 앱 Descriptor 정보 GET API를 라우터에 추가
        self.api_router.add_api_route(self.descriptor_url, self._get_app_descriptor, methods=['GET'])
        self._logger.debug('connect descriptor route added. (url)'.format(url=self.descriptor_url))

        self.app.include_router(self.api_router)

    async def _get_app_descriptor(self):
        return self.descriptor
