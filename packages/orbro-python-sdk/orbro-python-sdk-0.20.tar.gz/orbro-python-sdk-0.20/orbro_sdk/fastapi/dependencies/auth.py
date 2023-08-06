import json, logging
from fastapi import Depends, Header, HTTPException
from typing import Union
from orbro_sdk.constants import WEBHOOK_USER_AGENT
from orbro_sdk.datastore import ClientInfoDataStore
from orbro_sdk.util import get_origin_from_subdomain
from orbro_sdk.app import OrbroConnect

logger = logging.getLogger(__name__)


async def webhook_auth_dep(
    authorization: str = Header(default=''),
    client_datastore: ClientInfoDataStore = Depends(OrbroConnect.client_info_store_dep)
):
    logger.debug('webhook_auth_dep: header info authorization -> '
                 '{authorization}'.format(authorization=authorization))
    token = authorization.replace('Bearer ', '')

    try:
        payload = OrbroConnect.token_util.decode_token(None, token, False)
        issued_by = payload.get('issued_by')

        if issued_by != WEBHOOK_USER_AGENT:
            raise HTTPException(status_code=401, detail='Invalid Issuer. This is not webhook service token.')

        subject = payload.get('sub')

        if subject:
            uuid = subject.replace("uuid:", "") if 'uuid' in subject else None
            organization_id = subject.replace("organizationId:", "") if 'organizationId' in subject else None
            if organization_id:
                client_info = client_datastore.get_by_organization_id(organization_id)
            elif uuid:  # TODO: 현재 Webhook 서비스에서 발급되는 토큰은 uuid를 subject로 활용하지 않음.
                client_info = client_datastore.get_by_user_id(uuid)
            else:
                raise HTTPException(status_code=401, detail='Invalid subject')

            if client_info:
                shared_secret = client_info.shared_secret
                try:
                    OrbroConnect.token_util.decode_token(shared_secret, token)
                    return {
                        'organization_id': client_info.organization_id,
                        'user_id': client_info.installed_user_id
                    }
                except Exception as e:
                    raise HTTPException(status_code=401, detail=str(e))
            else:
                raise HTTPException(status_code=401,
                                    detail='Invalid client information. '
                                           'The client needs to check whether the app has been installed normally.')
        else:
            raise HTTPException(status_code=401, detail='Invalid subject')
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def request_auth_dep(
    authorization: str = Header(default=''),
    origin: Union[str, None] = None,
    sub: Union[str, None] = Header(default=None)
):
    logger.debug('request_auth_dep: header info authorization -> '
                 '{authorization}'.format(authorization=authorization))
    token = authorization.replace('Bearer ', '')
    sub = get_origin_from_subdomain(sub, OrbroConnect.host)
    origin = origin if origin is not None else sub
    logger.debug('request_auth_dep: header info sub -> {sub} / origin -> {origin}'.format(origin=origin, sub=sub))
    try:
        OrbroConnect.token_util.decode_web_token(token)
        r = await OrbroConnect.token_util.async_verify_web_token_by_remote(token, origin)
        res = json.loads(r.text)
        return res
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def request_connect_app_auth_dep(
    authorization: str = Header(default=''),
    origin: Union[str, None] = None,
    sub: Union[str, None] = Header(default=None)
):
    logger.debug('request_connect_app_auth_dep: header info authorization -> '
                 '{authorization}'.format(authorization=authorization))
    token = authorization.replace('Bearer ', '')
    sub = get_origin_from_subdomain(sub, OrbroConnect.host)
    origin = origin if origin is not None else sub
    logger.debug('request_auth_dep: header info sub -> {sub} / origin -> {origin}'.format(origin=origin, sub=sub))

    try:
        OrbroConnect.token_util.decode_web_token(token)
        r = await OrbroConnect.token_util.async_verify_connect_app_token_by_remote(token, origin)
        res = json.loads(r.text)
        return res
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def request_oauth_dep(
    authorization: str = Header(default='')
):
    logger.debug('request_oauth_dep: header info authorization -> '
                 '{authorization}'.format(authorization=authorization))
    token = authorization.replace('Bearer ', '')

    try:
        r = await OrbroConnect.token_util.async_verify_oauth_token_by_remote(token)
        res = json.loads(r.text)
        return res
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
