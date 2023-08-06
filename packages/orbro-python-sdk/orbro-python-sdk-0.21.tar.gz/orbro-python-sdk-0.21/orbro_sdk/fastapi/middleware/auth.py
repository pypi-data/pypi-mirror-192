import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from orbro_sdk import OrbroConnect
from orbro_sdk.util import get_origin_from_subdomain, get_subdomain_from_url

logger = logging.getLogger(__name__)


class ConnectAppAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # origin, sub, token 꺼내서 검증
        headers = request.headers
        query_params = request.query_params
        authorization = headers.get('Authorization')
        logger.debug('ConnectAppAuthMiddleware: headers -> {headers}'.format(headers=headers))
        # Web에서 사용
        origin = query_params.get('origin', None)

        # Mobile에서 organization의 subdomain으로 사용
        sub = headers.get('sub')
        sub = get_origin_from_subdomain(sub, OrbroConnect.host)
        origin = origin if origin is not None else sub
        logger.debug('ConnectAppAuthMiddleware: sub -> {sub} / origin -> {origin}'.format(origin=origin, sub=sub))
        # Web Token Decode 처리
        if authorization and origin:
            # 요청된 Host와 플랫폼에서 전달받은 Origin 검증
            # TODO: ORIGIN 검증 추가 필요. (현재는 API 호출 시 플랫폼에서 검증함.)
            try:
                payload = OrbroConnect.token_util.decode_web_token(authorization.replace('Bearer ', ''))
                if payload:
                    email = payload.get('data')
                    subdomain = get_subdomain_from_url(origin)
                    logger.debug(
                        'ConnectAppAuthMiddleware: parsed subdomain -> {subdomain}'.format(subdomain=subdomain))
                    if email:
                        request.state.user = {
                            'email': payload.get('data'),
                            'origin': origin,
                            'subdomain': subdomain
                        }
                    else:
                        raise HTTPException(status_code=401,
                                            detail='Invalid Token. There is no payload data.')
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))
        res = await call_next(request)
        return res

