"""
Jacobson is a self hosted zipcode API
Copyright (C) 2023-2024  Christian G. Semke.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op

"""
Create State, City and Address tables.

Revision ID: c13b281db692
Revises:
Create Date: 2024-05-23 17:35:33.396865

"""

# revision identifiers, used by Alembic.
revision: str = 'c13b281db692'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create State, City and Address tables based on sqlmodel metadata."""
    op.create_table(
        'city',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ibge', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('ddd', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ibge'),
    )
    op.create_table(
        'state',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'acronym',
            sa.Enum(
                'AC',
                'AL',
                'AP',
                'AM',
                'BA',
                'CE',
                'DF',
                'ES',
                'GO',
                'MA',
                'MT',
                'MS',
                'MG',
                'PA',
                'PB',
                'PR',
                'PE',
                'PI',
                'RJ',
                'RN',
                'RS',
                'RO',
                'RR',
                'SC',
                'SP',
                'SE',
                'TO',
                name='stateacronym',
            ),
            nullable=False,
        ),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('acronym'),
    )
    op.create_table(
        'address',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zipcode', sa.Integer(), nullable=False),
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.Column('city_id', sa.Integer(), nullable=False),
        sa.Column(
            'neighborhood', sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            'complement', sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ['city_id'],
            ['city.id'],
        ),
        sa.ForeignKeyConstraint(
            ['state_id'],
            ['state.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('zipcode'),
    )


def downgrade() -> None:
    """Drop address, state and city tables."""
    op.drop_table('address')
    op.drop_table('state')
    op.drop_table('city')
