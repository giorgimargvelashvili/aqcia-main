"""Make Category.name nullable

Revision ID: 6305da30268d
Revises: b466d0d02c8f
Create Date: 2025-07-21 12:13:57.874594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6305da30268d'
down_revision: Union[str, Sequence[str], None] = 'b466d0d02c8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
        # Step 1: Populate the 'name' column from 'name_en' for all rows
        op.execute('UPDATE categories SET name = name_en WHERE name IS NULL')

        # Step 2: Add the NOT NULL constraint
        op.alter_column('categories', 'name', nullable=False)

        # Step 3: Add the UNIQUE constraint
        op.create_unique_constraint('uq_categories_name', 'categories', ['name'])

def downgrade():
        # Reverse the operations
        op.drop_constraint('uq_categories_name', 'categories', type_='unique')
        op.alter_column('categories', 'name', nullable=True)
        # The data change (name -> name_en) is not easily reversible