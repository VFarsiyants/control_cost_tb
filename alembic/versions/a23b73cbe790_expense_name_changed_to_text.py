"""Expense name changed to text

Revision ID: a23b73cbe790
Revises: bdec385f81d8
Create Date: 2023-06-18 12:42:34.976162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a23b73cbe790'
down_revision = 'bdec385f81d8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("expense", "name", type_=sa.Text, nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("expense", "name", type_=sa.String(length=30), nullable=True)
    # ### end Alembic commands ###
