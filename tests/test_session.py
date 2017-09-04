from mlhoops.db.session import get_db
from mlhoops.db import engine


def test_session():
    db = get_db()
    assert db.get_bind() is engine
