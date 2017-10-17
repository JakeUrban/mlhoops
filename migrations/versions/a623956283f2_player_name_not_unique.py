"""player name not unique

Revision ID: a623956283f2
Revises: acdfe84c7fcf
Create Date: 2017-10-16 14:58:26.085956

"""
from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = 'a623956283f2'
down_revision = 'acdfe84c7fcf'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('players', 'name')
    op.add_column('players', Column('name', String(255), nullable=False))


def downgrade():
    op.drop_column('players', 'name')
    op.add_column('players', Column('name', String(255), unique=True,
                                    nullable=False))
