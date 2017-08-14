"""added season table

Revision ID: eee819d697c1
Revises: 3a339b210096
Create Date: 2017-08-13 12:25:56.477665

"""
from alembic import op
from sqlalchemy import Column, Integer


# revision identifiers, used by Alembic.
revision = 'eee819d697c1'
down_revision = '3a339b210096'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('seasons',
        Column('id', Integer(), primary_key=True),
        Column('year', Integer(), nullable=False, unique=True)
    )


def downgrade():
    op.drop_table('seasons')
