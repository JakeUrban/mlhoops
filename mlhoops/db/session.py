from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g
from os import environ

engine = create_engine(environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://Jake@localhost/mlhoops')
)

Base = declaritive_base(bind=engine)


def get_db():
    try:
        if not hasattr(g, 'session'):
            g.session = sessionmaker(bind=engine)()
        return g.session
    except RuntimeError:
        return sessionmaker(bind=engine)()


session = get_db()
