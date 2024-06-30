"""update association table -> unique constraint

Revision ID: b9d6e94f5d19
Revises: 26f1e2c8a674
Create Date: 2024-07-01 03:13:40.400000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9d6e94f5d19'
down_revision: Union[str, None] = '26f1e2c8a674'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project_users', 'project_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('project_users', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.create_unique_constraint('uq_project_user', 'project_users', ['project_id', 'user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_project_user', 'project_users', type_='unique')
    op.alter_column('project_users', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('project_users', 'project_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###
