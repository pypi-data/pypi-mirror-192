"""
    1) FastAPI Async 동작에 SDK가 DB Session을 유지하기 위해 하기 출처의 오픈 소스 변경하여 사용
    - 출처 : https://github.com/mfreeborn/fastapi-sqlalchemy
    2) 기타 Github 연관 Question 이슈
    - https://github.com/tiangolo/fastapi/issues/726

"""
from contextvars import ContextVar
from typing import Dict, Optional
from sqlalchemy.orm import Session, sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from orbro_sdk.exceptions import MissingSessionError, SessionNotInitialisedError

_Session: sessionmaker = None
_session: ContextVar[Optional[Session]] = ContextVar("_session", default=None)


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        session: sessionmaker,
        commit_on_exit: bool = False,
    ):
        super().__init__(app)
        global _Session
        self.commit_on_exit = commit_on_exit
        _Session = session

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        with db(commit_on_exit=self.commit_on_exit):
            response = await call_next(request)
        return response


class DBSessionMeta(type):
    # using this metaclass means that we can access db.session as a property at a class level,
    # rather than db().session
    @property
    def session(self) -> Session:
        """Return an instance of Session local to the current async context."""
        if _Session is None:
            raise SessionNotInitialisedError

        session = _session.get()
        if session is None:
            raise MissingSessionError

        return session


class DBSession(metaclass=DBSessionMeta):
    def __init__(self, session_args: Dict = None, commit_on_exit: bool = False):
        self.token = None
        self.session_args = session_args or {}
        self.commit_on_exit = commit_on_exit

    def __enter__(self):
        if not isinstance(_Session, sessionmaker):
            raise SessionNotInitialisedError
        self.token = _session.set(_Session(**self.session_args))
        return type(self)

    def __exit__(self, exc_type, exc_value, traceback):
        sess = _session.get()
        if exc_type is not None:
            sess.rollback()

        if self.commit_on_exit:
            sess.commit()

        sess.close()
        _session.reset(self.token)


db: DBSessionMeta = DBSession
