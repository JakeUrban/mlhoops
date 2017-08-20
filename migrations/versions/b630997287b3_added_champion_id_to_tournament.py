"""Added champion_id to tournament

Revision ID: b630997287b3
Revises: ba8e2c013873
Create Date: 2017-08-20 15:15:40.157379

"""
from alembic import op
from sqlalchemy import Column, ForeignKey, Integer


# revision identifiers, used by Alembic.
revision = 'b630997287b3'
down_revision = 'ba8e2c013873'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tournaments',
                  Column('champion_id', Integer, ForeignKey('teams.id')))


def downgrade():
    op.drop_constraint('tournaments_ibfk_2', 'tournaments', type_='foreignkey')
    op.drop_column('tournaments', 'champion_id')
