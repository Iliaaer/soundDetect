"""init

Revision ID: d91cc0848fa1
Revises: 
Create Date: 2023-04-24 22:17:43.274915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd91cc0848fa1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audiofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('time', sa.TIMESTAMP(), nullable=True),
    sa.Column('device', sa.String(), nullable=True),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('result', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audiofile_id'), 'audiofile', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_audiofile_id'), table_name='audiofile')
    op.drop_table('audiofile')
    # ### end Alembic commands ###
