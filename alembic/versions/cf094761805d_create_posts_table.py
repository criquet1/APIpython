"""Create posts table

Revision ID: cf094761805d
Revises: 
Create Date: 2022-01-31 11:40:34.193195
1ère revision
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf094761805d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(),
                              nullable=False, server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('NOW()')),
                    sa.Column('owner_id', sa.Integer(), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
