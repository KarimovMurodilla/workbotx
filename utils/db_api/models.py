from distutils.sysconfig import get_makefile_filename
from sqlalchemy import Column, BigInteger, Float

from utils.db_api.base import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    balance = Column(Float)