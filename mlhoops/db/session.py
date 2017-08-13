from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import g


def get_db():
    engine = create_engine('mysql+pymysql://Jake@localhost/mlhoops')
    if not hasattr(g, 'session'):
        g.session = sessionmaker(bind=engine)()
    return g.session


Base = declarative_base()
session = get_db()
