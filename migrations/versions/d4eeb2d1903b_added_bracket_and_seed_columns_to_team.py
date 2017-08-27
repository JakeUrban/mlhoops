"""Added bracket and seed columns to team

Revision ID: d4eeb2d1903b
Revises: 16d2f5556780
Create Date: 2017-08-26 20:30:21.072786

"""
from alembic import op
from sqlalchemy import Column, String, Integer


# revision identifiers, used by Alembic.
revision = 'd4eeb2d1903b'
down_revision = '16d2f5556780'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('teams', Column('bracket', String(255)))
    op.add_column('teams', Column('seed', Integer))

def downgrade():
    op.drop_column('teams', 'bracket')
    op.drop_column('teams', 'seed')
