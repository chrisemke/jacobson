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
Create users table

Revision ID: b065b6143c4f
Revises: 16486dde779e
Create Date: 2024-08-06 03:10:40.866976

"""

# revision identifiers, used by Alembic.
revision: str = 'b065b6143c4f'
down_revision: str | None = '16486dde779e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	"""Create users table."""
	op.create_table(
		'users',
		sa.Column('id', sa.Uuid(), nullable=False),
		sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
		sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
		sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
		sa.PrimaryKeyConstraint('id'),
	)
	op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
	"""Drop users table."""
	op.drop_index(op.f('ix_users_email'), table_name='users')
	op.drop_table('users')
