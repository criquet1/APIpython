"""Create users table

Revision ID: c86d65f40a61
Revises: cf094761805d
Create Date: 2022-01-31 12:24:05.287282
2e révision = cette revision n'a pas fonctionné, j'en ai refait une autre juste après
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c86d65f40a61'
down_revision = 'cf094761805d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
