"""no home or away teams

Revision ID: 16d2f5556780
Revises: 56011e173201
Create Date: 2017-08-20 20:12:28.738080

"""
from alembic import op
from sqlalchemy import Integer


# revision identifiers, used by Alembic.
revision = '16d2f5556780'
down_revision = '56011e173201'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('games', 'home_team', new_column_name='team_one',
                    existing_type=Integer, existing_nullable=False)
    op.alter_column('games', 'away_team', new_column_name='team_two',
                    existing_type=Integer, existing_nullable=False)
    op.alter_column('games', 'home_team_score',
                    new_column_name='team_one_score', existing_type=Integer,
                    existing_nullable=False)
    op.alter_column('games', 'away_team_score',
                    new_column_name='team_two_score', existing_type=Integer,
                    existing_nullable=False)


def downgrade():
    op.alter_column('games', 'team_one', new_column_name='home_team',
                    existing_type=Integer, existing_nullable=False)
    op.alter_column('games', 'team_two', new_column_name='away_team',
                    existing_type=Integer, existing_nullable=False)
    op.alter_column('games', 'team_one_score',
                    new_column_name='home_team_score', existing_type=Integer,
                    existing_nullable=False)
    op.alter_column('games', 'team_two_score',
                    new_column_name='away_team_score', existing_type=Integer,
                    existing_nullable=False)
