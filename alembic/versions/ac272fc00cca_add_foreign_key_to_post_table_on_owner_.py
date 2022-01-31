"""add foreign key to post table on owner_id column

Revision ID: ac272fc00cca
Revises: ff8dffbdeb11
Create Date: 2022-01-31 12:52:00.013797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac272fc00cca'
down_revision = 'ff8dffbdeb11'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk')
    pass
