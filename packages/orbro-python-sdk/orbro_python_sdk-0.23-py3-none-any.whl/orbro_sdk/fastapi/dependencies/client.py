import logging
from fastapi import Depends, Header, HTTPException
from typing import Union
from orbro_sdk import OrbroConnect
from orbro_sdk.util import get_origin_from_subdomain
from orbro_sdk.datastore import ClientInfoDataStore, RedisTokenDataStore, DictTokenDataStore
from orbro_sdk.async_client import AsyncWebClient

logger = logging.getLogger(__name__)


async def get_async_client(
    origin: Union[str, None] = None,
    sub: Union[str, None] = Header(default=None),
    client_datastore: ClientInfoDataStore = Depends(OrbroConnect.client_info_store_dep),
    token_store: Union[RedisTokenDataStore, DictTokenDataStore] = Depends(OrbroConnect.token_store_dep)
):
    sub = get_origin_from_subdomain(sub, OrbroConnect.host)
    origin = origin if origin is not None else sub
    logger.debug('get_async_client: header info sub -> {sub} / origin -> {origin}'.format(origin=origin, sub=sub))
    async_webclient = AsyncWebClient(client_datastore=client_datastore, token_store=token_store,
                                     token_util=OrbroConnect.token_util, origin=origin)
    return async_webclient


async def get_openapi_async_client(
    origin: Union[str, None] = None,
    sub: Union[str, None] = Header(default=None),
    client_datastore: ClientInfoDataStore = Depends(OrbroConnect.client_info_store_dep),
    token_store: Union[RedisTokenDataStore, DictTokenDataStore] = Depends(OrbroConnect.token_store_dep)
):
    sub = get_origin_from_subdomain(sub, OrbroConnect.host)
    origin = origin if origin is not None else sub
    logger.debug('get_async_client: header info sub -> {sub} / origin -> {origin}'.format(origin=origin, sub=sub))
    async_webclient = AsyncWebClient(client_datastore=client_datastore, token_store=token_store,
                                     token_util=OrbroConnect.token_util, origin=origin,
                                     open_api_token=OrbroConnect.open_api_token)

    return async_webclient
