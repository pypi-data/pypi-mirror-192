import logging
from .constants import DEFAULT_TOKEN_EXPIRES_IN
from .models import ConnectAppToken


class DataStore(object):
    def __init__(self, db):
        self.db = db
        self._logger = logging.getLogger(__name__)

    def set_db(self, db):
        self.db = db

    def commit(self):
        pass

    def add(self, model):
        pass

    def delete(self, model):
        raise NotImplementedError


class SQLAlchemyDataStore(DataStore):
    def __init__(self, db):
        super().__init__(db)

    def commit(self):
        self.db.commit()

    def add(self, model):
        self.db.add(model)
        return model

    def delete(self, model):
        self.db.delete(model)


class KeyValueDataStore(DataStore):
    def __init__(self, db):
        super().__init__(db)

    def set(self, key, value, expires=None):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError


class RedisDataStore(KeyValueDataStore):
    def __init__(self, db):
        super().__init__(db)

    def set(self, key, value, expires=None):
        self.db.set(key, value, px=expires)

    def get(self, key):
        if key:
            value = self.db.get(key)
            if value is not None:
                return value
        return None

    def delete(self, key):
        item = self.db.get(key)
        if item is not None:
            self.db.delete(key)


class DictDataStore(KeyValueDataStore):
    def __init__(self, db={}):
        super().__init__(db)

    def set(self, key, value, expires=None):
        self.db[key] = value

    def get(self, key):
        if key:
            return self.db.get(key, None)
        return None

    def delete(self, key):
        item = self.db.get(key, None)
        if item is not None:
            del self.db[key]


class ClientInfoDataStore(SQLAlchemyDataStore):
    def __init__(self, db, client_info_model):
        super().__init__(db)
        self.model = client_info_model

    def add(self, data: dict):
        data['installed_user_id'] = data.pop('user_id', None)
        client_info = self.model(**data)
        client_info = super().add(client_info)
        return client_info

    def get_by_organization_id(self, organization_id):
        return self.db.query(self.model).\
            filter_by(organization_id=organization_id).first()

    def get_by_subdomain(self, subdomain):
        return self.db.query(self.model).\
            filter_by(subdomain=subdomain).first()

    def get_by_user_id(self, user_id):
        return self.db.query(self.model).\
            filter_by(installed_user_id=user_id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def delete(self, client_info):
        super().delete(client_info)


class DictTokenDataStore(DictDataStore):
    def set_token(self, token_model):
        if isinstance(token_model, ConnectAppToken):
            self.set(token_model.organization_id, token_model.access_token)
        elif isinstance(token_model, dict) and token_model.get('organization_id'):
            self.set(token_model.get('organization_id'), token_model.get('access_token'))
        else:
            self._logger.error('Invalid token_model')

    def get_token(self, organization_id):
        token = self.get(organization_id)
        if token:
            return ConnectAppToken(organization_id=organization_id, access_token=token)
        return token


class RedisTokenDataStore(RedisDataStore):
    def set_token(self, token_model, expires=DEFAULT_TOKEN_EXPIRES_IN):
        # token_model이 class인지 체크하여 분기 처리
        if isinstance(token_model, ConnectAppToken):
            self.set(token_model.organization_id, token_model.access_token, expires)
        elif isinstance(token_model, dict) and token_model.get('organization_id'):
            self.set(token_model.get('organization_id'), token_model.get('access_token'), expires)
        else:
            self._logger.error('Invalid token_model')

    def get_token(self, organization_id):
        token = self.get(organization_id)
        if token:
            return ConnectAppToken(organization_id=organization_id, access_token=token)
        return token







