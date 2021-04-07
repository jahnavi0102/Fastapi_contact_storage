"""create contacts table

Revision ID: 84238cbc5520
Revises: 9ec29882b78d
Create Date: 2021-04-07 16:36:25.992295

"""
from alembic import op
import sqlalchemy as sa
from models import User 


# revision identifiers, used by Alembic.
revision = '84238cbc5520'
down_revision = '9ec29882b78d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('phone', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50),nullable=False),
        sa.Column('owner_id', sa.Integer,sa.ForeignKey('User.id'))
       
    )



def downgrade():
    op.drop_table('contacts')
