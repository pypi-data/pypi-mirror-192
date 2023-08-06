import httpx, jwt, logging, base64, json, re
from .constants import DEFAULT_TOKEN_EXPIRES_IN, DEFAULT_ISSUER, DEFAULT_TIMEOUT, \
    CONNECT_APP_ISSUE_TOKEN_URL, CONNECT_APP_AUTH_URL, AUTH_URL, OAUTH_URL
from datetime import datetime, timedelta


def get_subdomain_from_url(origin):
    remove_prefix = re.compile(r"https?://(www\.)?")
    refined_origin = remove_prefix.sub('', origin).strip().strip('/')
    subdomain = refined_origin.split('.')[0]
    return subdomain


def get_origin_from_subdomain(subdomain, host):
    sub = f'https://{subdomain}.{host}' if subdomain is not None else ''
    return sub


class TokenUtil:
    DEFAULT_ALGORITHM = 'HS256'

    def __init__(self, client_id, client_secret, host=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.encoded_username = base64.b64encode(f'{self.client_id}:{self.client_secret}'
                                                 .encode('ascii')).decode('utf-8')
        if host:
            self.host = host
            self.base_url = 'https://{host}'.format(host=self.host)
        self._logger = logging.getLogger(__name__)

    def issue_token(self, shared_secret_key, user_id,
                    expires_in=DEFAULT_TOKEN_EXPIRES_IN):
        issued_at = datetime.utcnow()
        expire = issued_at + timedelta(milliseconds=expires_in)

        payload = {
            'iss': self.client_id,
            'exp': expire,
            'iat': issued_at,
            'sub': 'uuid:{user_id}'.format(user_id=user_id),
            'issued_by': DEFAULT_ISSUER
        }
        return jwt.encode(payload, shared_secret_key, algorithm=TokenUtil.DEFAULT_ALGORITHM)

    def decode_token(self, shared_secret_key, token, verify_signature=True):
        try:
            if verify_signature:
                payload = jwt.decode(token, shared_secret_key, algorithms=TokenUtil.DEFAULT_ALGORITHM)
            else:
                payload = jwt.decode(token, options={'verify_signature': verify_signature})
            return payload
        except jwt.ExpiredSignatureError:
            self._logger.error('Token has expired')
            raise
        except jwt.InvalidTokenError:
            self._logger.error('Invalid token')
            raise
        except Exception as e:
            self._logger.error(e)
            raise
        raise Exception('Invalid token')

    def decode_web_token(self, token):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except jwt.ExpiredSignatureError:
            self._logger.error('Web Token has expired')
            raise
        except Exception as e:
            self._logger.error(e)
            raise
        raise Exception('Invalid token')

    def _create_header(self, token=None, origin=None):
        if token:
            if 'Bearer' in token:
                header_token = token
            else:
                header_token = 'Bearer {token}'.format(token=token)

            headers = {
                'Authorization': header_token,
                'Content-Type': 'application/json'
            }
        else:
            headers = {
                'Content-Type': 'application/json'
            }
        return headers

    def _create_body(self, token, origin):
        if 'Bearer' in token:
            token = token.replace('Bearer ', '')
        body = {
            'username': self.encoded_username,
            'password': token,
            'origin': origin
        }
        return body

    def issue_app_token_by_remote(self, token, origin):
        headers = self._create_header()
        body = self._create_body(token, origin)
        url = self.base_url + CONNECT_APP_ISSUE_TOKEN_URL
        try:
            res = httpx.post(url, headers=headers, json=body, timeout=DEFAULT_TIMEOUT)
            return res
        except httpx.RemoteProtocolError as e:
            self._logger.error(e)
            raise
        except httpx.ReadTimeout as e:
            self._logger.error(e)
            raise

    async def async_issue_app_token_by_remote(self, token, origin):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            headers = self._create_header()
            body = self._create_body(token, origin)
            url = self.base_url + CONNECT_APP_ISSUE_TOKEN_URL
            req = client.build_request('POST', url, headers=headers, json=body)
            try:
                res = await client.send(req)
                return res
            except httpx.RemoteProtocolError as e:
                self._logger.error(e)
                raise
            except httpx.ReadTimeout as e:
                self._logger.error(e)
                raise

    # 플랫폼에서 발급 받은 토큰을 플랫폼에 인증 받는다.
    def verify_web_token_by_remote(self, token, origin):
        headers = self._create_header(token)
        url = f'{origin}' + AUTH_URL
        try:
            res = httpx.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
            return res
        except httpx.RemoteProtocolError as e:
            self._logger.error(e)
            raise e
        except httpx.ReadTimeout as e:
            self._logger.error(e)
            raise e

    async def async_verify_web_token_by_remote(self, token, origin):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            headers = self._create_header(token)
            url = f'{origin}' + AUTH_URL
            req = client.build_request('GET', url, headers=headers)
            try:
                res = await client.send(req)
                return res
            except httpx.RemoteProtocolError as e:
                self._logger.error(e)
                raise e
            except httpx.ReadTimeout as e:
                self._logger.error(e)
                raise e

    def verify_connect_app_token_by_remote(self, token, origin):
        headers = self._create_header(token)
        url = f'{origin}' + CONNECT_APP_AUTH_URL
        try:
            res = httpx.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
            return res
        except httpx.RemoteProtocolError as e:
            self._logger.error(e)
            raise e
        except httpx.ReadTimeout as e:
            self._logger.error(e)
            raise e

    async def async_verify_connect_app_token_by_remote(self, token, origin):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            headers = self._create_header(token)
            url = f'{origin}' + CONNECT_APP_AUTH_URL
            req = client.build_request('GET', url, headers=headers)
            try:
                res = await client.send(req)
                return res
            except httpx.RemoteProtocolError as e:
                self._logger.error(e)
                raise e
            except httpx.ReadTimeout as e:
                self._logger.error(e)
                raise e

    async def async_verify_oauth_token_by_remote(self, token):
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            headers = self._create_header(token)
            url = f'https://{self.host}' + OAUTH_URL
            req = client.build_request('GET', url, headers=headers)
            try:
                res = await client.send(req)
                return res
            except httpx.RemoteProtocolError as e:
                self._logger.error(e)
                raise e
            except httpx.ReadTimeout as e:
                self._logger.error(e)
                raise e
