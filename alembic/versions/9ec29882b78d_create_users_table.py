"""create users table

Revision ID: 9ec29882b78d
Revises: 
Create Date: 2021-04-07 16:36:16.880956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ec29882b78d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean),
       
    )


def downgrade():
    op.drop_table('users')
