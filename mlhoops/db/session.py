from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

engine = create_engine(environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://Jake@localhost/mlhoops')
)

Base = declarative_base(bind=engine)


def get_db():
    return sessionmaker(bind=engine)()
