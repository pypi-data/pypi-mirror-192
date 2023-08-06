from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from redis import Redis
from orbro_sdk.datastore import ClientInfoDataStore, RedisTokenDataStore, DictTokenDataStore


class ClientInfoStoreDep:
    def __init__(self, db: sessionmaker, client_info_store: ClientInfoDataStore):
        self.db_session = db
        self.client_info_store = client_info_store

    def __call__(self):
        db = self.db_session()
        self.client_info_store.set_db(db)
        try:
            yield self.client_info_store
        finally:
            db.close()


class RedisTokenStoreDep:
    def __init__(self, redis: Redis, token_store: RedisTokenDataStore):
        self.redis = redis
        self.token_store = token_store

    def __call__(self):
        self.token_store.set_db(self.redis)
        return self.token_store


class DictTokenStoreDep:
    def __init__(self, token_store: DictTokenDataStore):
        self.token_store = token_store

    def __call__(self):
        return self.token_store
