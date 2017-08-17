from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g
from os import environment

engine = create_engine(environment.get(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://Jake@localhost/mlhoops')
)


def get_db():
    if not hasattr(g, 'session'):
        g.session = sessionmaker(bind=engine)()
    return g.session


session = get_db()
