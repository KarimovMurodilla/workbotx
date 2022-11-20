from distutils.sysconfig import get_makefile_filename
from sqlalchemy import Column, BigInteger, Float, String

from utils.db_api.base import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    balance = Column(Float)


class Admin(Base):
    __tablename__ = "admin"

    just_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    name = Column(String)
    status = Column(String)