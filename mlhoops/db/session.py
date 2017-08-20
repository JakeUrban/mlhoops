from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g
from os import environ

engine = create_engine(environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://Jake@localhost/mlhoops')
)

Base = declarative_base(bind=engine)

# we use this global variable in place of flask's g object when
# we need a database connection outside of the apps context
OUT_OF_CONTEXT_SESSION = None


def get_db():
    try:
        if not hasattr(g, 'session'):
            g.session = sessionmaker(bind=engine)()
        return g.session
    except RuntimeError:  # pragma: no cover
        global OUT_OF_CONTEXT_SESSION
        if not OUT_OF_CONTEXT_SESSION:
            OUT_OF_CONTEXT_SESSION = sessionmaker(bind=engine)()
        return OUT_OF_CONTEXT_SESSION
