"""merge multiple heads

Revision ID: d8bdf0640bd7
Revises: 1234567890ab, xxxxxxxxxxxx
Create Date: 2025-05-06 19:00:46.807508+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8bdf0640bd7'
down_revision: Union[str, None] = ('1234567890ab', 'xxxxxxxxxxxx')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
