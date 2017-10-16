from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

from mlhoops import config

engine = create_engine(environ.get(
    'SQLALCHEMY_DATABASE_URI',
    config.SQLALCHEMY_DATABASE_URI)
)

Base = declarative_base(bind=engine)


def get_db():
    if not hasattr(config, 'session'):
        config.session = sessionmaker(bind=engine)()
    return config.session
