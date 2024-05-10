"""create user table

Revision ID: c7551e4de2ef
Revises: 
Create Date: 2024-05-06 11:49:32.116188

"""
from typing import Sequence

import sqlmodel
from alembic import op
import sqlalchemy as sa
import sqlmodel as sa


# revision identifiers, used by Alembic.
revision: str = 'c7551e4de2ef'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

    
def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer, primary_key=True, autoincrement=True ),
                    sa.Column("name", sa.Text),
                    sa.Column("phone_number",sa.TEXT)
    )

def downgrade() -> None:
    op.drop_table("users")
