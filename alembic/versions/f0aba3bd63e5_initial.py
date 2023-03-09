"""Initial

Revision ID: f0aba3bd63e5
Revises: 
Create Date: 2023-03-09 14:22:56.837457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0aba3bd63e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('secrets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('is_ended', sa.Boolean(), nullable=False),
    sa.Column('secret_id', sa.Integer(), nullable=False),
    sa.Column('winner_id', sa.BigInteger(), nullable=True),
    sa.Column('winner_points', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['secret_id'], ['secrets.id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    op.drop_table('secrets')
    op.drop_table('players')
    op.drop_table('admins')
    # ### end Alembic commands ###