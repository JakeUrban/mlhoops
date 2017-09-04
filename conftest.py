import pytest
from mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from mlhoops.db.init_db import init_db


engine = create_engine('sqlite://')


@pytest.fixture
def test_engine():
    return engine


@pytest.fixture
def session():
    session = sessionmaker(bind=engine)()

    def wrapper():
        return session
    Base = declarative_base(bind=engine)
    Base.metadata.reflect(bind=engine)
    patch('mlhoops.db.init_db.Base', Base)
    init_db(engine)
    yield wrapper
    wrapper().expunge_all()
    wrapper().close()
