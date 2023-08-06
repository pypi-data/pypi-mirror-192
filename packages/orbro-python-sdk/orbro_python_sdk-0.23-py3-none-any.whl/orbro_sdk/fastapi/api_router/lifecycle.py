import logging
from fastapi import Depends, HTTPException
from typing import Union
from orbro_sdk.models import InstalledAppInfo, UninstalledAppInfo
from orbro_sdk.datastore import ClientInfoDataStore, RedisTokenDataStore, DictTokenDataStore
from orbro_sdk.app import OrbroConnect

logger = logging.getLogger(__name__)


async def on_installed(req: InstalledAppInfo,
                       client_datastore: ClientInfoDataStore = Depends(OrbroConnect.client_info_store_dep),
                       token_store: Union[RedisTokenDataStore, DictTokenDataStore] = Depends(OrbroConnect.token_store_dep)):
    # installed 시점에 shared_secret 저장 및 토큰 발급하여 저장
    # 설치 시 organization_id, uuid, sharedSecretKey 저장
    organization_id = req.organization_id
    client_info = client_datastore.get_by_organization_id(organization_id)
    if not client_info:
        client_info = req.dict()
        client_datastore.add(client_info)
        logger.debug('installed: organization {org_id} app_client_info has been created.'.format(org_id=organization_id))
        token = OrbroConnect.token_util.issue_token(req.shared_secret, req.user_id)
        token_store.set(req.organization_id, token)
        logger.debug('installed: organization {org_id} '
                     'token has been created. ({token})'.format(org_id=organization_id, token=token))
        client_datastore.commit()
        return {'status_code': 200, 'detail': 'success'}
    else:
        logger.error('installed: Client information for an organization that already exists.')
        raise HTTPException(status_code=400, detail='This is an already installed app. '
                                                    'Client information for an organization that already exists.')


async def on_uninstalled(req: UninstalledAppInfo,
                         client_datastore: ClientInfoDataStore = Depends(OrbroConnect.client_info_store_dep),
                         token_store: Union[RedisTokenDataStore, DictTokenDataStore] = Depends(OrbroConnect.token_store_dep)):
    # uninstalled 시 organization_id, uuid, sharedSecretKey 삭제, 토큰 삭제
    organization_id = req.organization_id
    client_info = client_datastore.get_by_organization_id(organization_id)
    if client_info:
        client_datastore.delete(client_info)
        logger.debug('uninstalled: organization {org_id} app_client_info has been deleted.'.format(org_id=organization_id))
        token_store.delete(req.organization_id)
        logger.debug('uninstalled: organization {org_id} '
                     'token has been deleted.'.format(org_id=organization_id))
        client_datastore.commit()
    else:
        logger.error('uninstalled: Client information for an organization that already has been deleted.')
        raise HTTPException(status_code=400, detail='This is an already deleted app. '
                                                    'Client information for an organization that '
                                                    'already has been deleted')
