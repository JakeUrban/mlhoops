from alembic import command
from alembic.config import Config

from mlhoops.db.session import engine
from mlhoops.db.base import Base


def drop_db():
    Base.metadata.reflect(engine)
    tables = Base.metadata.tables.copy()
    tables.pop('alembic_version')
    Base.metadata.drop_all(tables=tables.values())


def init_db():
    alembic_cfg = Config('alembic.ini')
    command.stamp(alembic_cfg, "head")
    Base.metadata.create_all(engine)


def init_db_data():
    pass


if __name__ == '__main__':
    drop_db()
    init_db()
    init_db_data()
