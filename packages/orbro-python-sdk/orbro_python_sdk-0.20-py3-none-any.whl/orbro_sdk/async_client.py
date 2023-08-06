# API 호출 시, 토큰 존재하지 않거나 만료 시 토큰 자동 재발급
import logging, httpx, json
from typing import Union
from orbro_sdk import OrbroConnect
from orbro_sdk.constants import CONNECT_APP_USER_AGENT, DEFAULT_TIMEOUT, PLATFORM_TOKEN_EXPIRED_ERROR_CODE
from orbro_sdk.datastore import DictTokenDataStore, RedisTokenDataStore
from orbro_sdk.util import get_subdomain_from_url
from orbro_sdk.models import ConnectAppToken

logger = logging.getLogger(__name__)


class AsyncBaseClient:
    def __init__(
            self,
            sdk_app: OrbroConnect):
        self.sdk_app = sdk_app

    async def get(self, url):
        raise NotImplementedError

    async def post(self, url):
        raise NotImplementedError

    async def put(self, url):
        raise NotImplementedError

    async def delete(self, url):
        raise NotImplementedError

    async def head(self, url):
        raise NotImplementedError

    async def options(self, url):
        raise NotImplementedError

    async def send(self, request):
        raise NotImplementedError


class AsyncWebClient(AsyncBaseClient):
    def __init__(self, sdk_app=None, client_datastore=None, token_store=None, token_util=None, origin=None,
                 open_api_token=None):
        super().__init__(sdk_app)
        if sdk_app:  # 글로벌로 사용하는 경우
            self.client_datastore = sdk_app.client_info_datastore()
            self.token_store: Union[RedisTokenDataStore, DictTokenDataStore] = sdk_app.token_store
            self.token_util = sdk_app.token_util
            self.host = sdk_app.host
        else:   # Depends를 통해 주입된 경우
            self.client_datastore = client_datastore
            self.token_store: Union[RedisTokenDataStore, DictTokenDataStore] = token_store
            self.token_util = token_util
            self.origin = origin
            self.host = OrbroConnect.host
        self._logger = logging.getLogger(__name__)
        self.open_api_token = open_api_token

    def create_request(self, origin, url, custom_headers):
        if self.open_api_token:
            subdomain = ''
            headers = self.create_openapi_header(self.open_api_token)
            target_url = self.create_target_url(subdomain, url)
        else:
            subdomain = get_subdomain_from_url(origin)
            headers = self.create_header(subdomain)
            target_url = self.create_target_url(subdomain, url)

        if custom_headers is not None and type(custom_headers) is dict:
            headers.update(custom_headers)

        return {
            'headers': headers,
            'url': target_url
        }

    def create_openapi_header(self, token):
        return {
            'Authorization': 'Bearer {token}'.format(token=token),
            'Content-Type': 'application/json'
        }

    def create_header(self, subdomain, token=None):
        if token is None:
            token = self.get_token_by_subdomain(subdomain)
        return {
            'Authorization': 'Bearer {token}'.format(token=token),
            'User-Agent': CONNECT_APP_USER_AGENT,
            'Content-Type': 'application/json'
        }

    def create_target_url(self, subdomain, url):
        if subdomain and subdomain != '':
            target_url = 'https://{subdomain}.{host}{url}'.format(subdomain=subdomain,
                                                                  host=self.host, url=url)
        else:   # Open API
            target_url = 'https://{host}{url}'.format(host=self.host, url=url)

        return target_url

    def get_token_by_subdomain(self, subdomain, is_refresh=False):
        client_info = self.client_datastore.get_by_subdomain(subdomain)
        if client_info is None:
            e = Exception('Invalid subdomain ''{domain}'' and client information. '
                          'The client needs to check whether the app '
                          'has been installed normally.'.format(domain=subdomain))
            self._logger.error(str(e))
            raise e
        organization_id = client_info.organization_id
        token: ConnectAppToken = self.token_store.get_token(organization_id)
        if not is_refresh and token and token.access_token:
            self._logger.debug('get_token_by_subdomain: Succeeded in '
                               'getting token as client information. ({token})'.format(token=token))
            return token.access_token
        else:
            self._logger.warning('organization ''{id}''token has expired or token has not yet been created. '
                                 'generated new token is saved.'.format(id=organization_id))
            token = self.token_util.issue_token(client_info.shared_secret, client_info.installed_user_id)
            self.token_store.set_token({
                'organization_id': organization_id,
                'access_token': token
            })
            return token

    def _verify_origin(self):
        if not self.origin and not self.open_api_token:
            e = Exception('AsyncWebClient has no origin information.')
            self._logger.error(str(e))
            raise e
        return self.origin

    async def get(self, url, headers=None, origin=None):
        if origin is None: # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('GET', req.get('url'), headers=req.get('headers'), origin=origin)

    async def post(self, url, data, headers=None, origin=None):
        if origin is None:  # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('POST', req.get('url'), headers=req.get('headers'), data=data, origin=origin)

    async def put(self, url, data, headers=None, origin=None):
        if origin is None:  # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('PUT', req.get('url'), headers=req.get('headers'), data=data, origin=origin)

    async def patch(self, url, data, headers=None, origin=None):
        if origin is None:  # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('PATCH', req.get('url'), headers=req.get('headers'), data=data, origin=origin)

    async def delete(self, url, headers=None, origin=None):
        if origin is None:  # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('DELETE', req.get('url'), headers=req.get('headers'), origin=origin)

    async def options(self, url, headers=None, origin=None):
        if origin is None:  # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('OPTIONS', req.get('url'), headers=req.get('headers'), origin=origin)

    async def head(self, url, headers=None, origin=None):
        if origin is None:  # Depends용
            origin = self._verify_origin()
        req = self.create_request(origin, url, headers)
        return await self.send('HEAD', req.get('url'), headers=req.get('headers'), origin=origin)

    async def send(self, method, url, headers, params=None, data=None, origin=None):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            req = client.build_request(method, url, headers=headers, params=params, json=data)
            try:
                res = await client.send(req)
                if res.status_code != 200:
                    r = json.loads(res.text)
                    # TODO: 토큰 만료 시, 자동으로 새 토큰 생성 및 재시도 (1회)
                    error_code = r.get('error_code')
                    if r and error_code == PLATFORM_TOKEN_EXPIRED_ERROR_CODE and origin and not self.open_api_token:
                        subdomain = get_subdomain_from_url(origin)
                        token = self.get_token_by_subdomain(subdomain, is_refresh=True)
                        headers = self.create_header(subdomain, token=token)
                        self.send(method, url, headers, params=params, data=data)
                return res
            except httpx.HTTPError as e:
                self._logger.error(str(e))
