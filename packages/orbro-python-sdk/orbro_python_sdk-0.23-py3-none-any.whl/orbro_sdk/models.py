from pydantic import BaseModel, Field
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as C_UUID
from typing import Optional
from sqlalchemy import (
    DateTime,
    Column,
    Integer,
    String
)
from sqlalchemy.sql import func


# Application Model
# TODO: descriptor (connect.json) 명세를 pydantic Model로 반영 필요.
class AppDescriptor(BaseModel):
    pass


class ConnectAppToken(BaseModel):
    organization_id: UUID = Field(..., description='Connnect 앱을 설치한 소속(조직)의 UUID')
    access_token: str = Field(..., description='설치된 Connect 앱에 발급된 Token')


# FastAPI Request Model
class InstalledAppInfo(BaseModel):
    shared_secret: str = Field(..., description='설치된 Connect 앱에 발급된 SharedSecret')
    user_id: Optional[str] = Field(None, description='Connect 앱을 설치한 유저의 UUID')
    organization_id: str = Field(..., description='Connnect 앱을 설치한 소속(조직)의 UUID')
    subdomain: str = Field(None, description='Connect 앱을 설치한 소속(조직)의 서브 도메인')


class UninstalledAppInfo(BaseModel):
    organization_id: str = Field(..., description='Connnect 앱을 설치한 소속(조직)의 UUID')


# Database Model
class ConnectAppClientInfoMixin:
    """Connect App Shared Secret Info"""
    __tablename__ = 'connect_app_client_info'
    id = Column(Integer, primary_key=True)
    organization_id = Column(String(255), nullable=False)
    shared_secret = Column(String(255), nullable=False)
    subdomain = Column(String(255))
    installed_user_id = Column(String(255))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now())
