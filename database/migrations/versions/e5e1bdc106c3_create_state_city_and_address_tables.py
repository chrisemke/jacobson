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
from sqlalchemy.dialects import postgresql

"""
Create States, Cities and Addresses tables.

Revision ID: e5e1bdc106c3
Revises:
Create Date: 2024-07-24 18:06:29.733492

"""

# revision identifiers, used by Alembic.
revision: str = 'e5e1bdc106c3'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	"""Create State, City and Address tables."""
	op.create_table(
		'cities',
		sa.Column('id', sa.Uuid(), nullable=False),
		sa.Column('ibge', sa.Integer(), nullable=False),
		sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
		sa.Column('ddd', sa.Integer(), nullable=True),
		sa.PrimaryKeyConstraint('id'),
	)
	op.create_index(op.f('ix_cities_ibge'), 'cities', ['ibge'], unique=True)
	op.create_table(
		'states',
		sa.Column('id', sa.Uuid(), nullable=False),
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
	)
	op.create_index(op.f('ix_states_acronym'), 'states', ['acronym'], unique=True)
	op.create_table(
		'addresses',
		sa.Column('id', sa.Uuid(), nullable=False),
		sa.Column('zipcode', sa.Integer(), nullable=False),
		sa.Column('state_id', sa.Uuid(), nullable=False),
		sa.Column('city_id', sa.Uuid(), nullable=False),
		sa.Column(
			'neighborhood', sqlmodel.sql.sqltypes.AutoString(), nullable=False
		),
		sa.Column('complement', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
		sa.Column(
			'coordinates',
			postgresql.JSONB(astext_type=sa.Text()),  # type: ignore[no-untyped-call]
			nullable=True,
		),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(
			['city_id'],
			['cities.id'],
		),
		sa.ForeignKeyConstraint(
			['state_id'],
			['states.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)
	op.create_index(
		op.f('ix_addresses_zipcode'), 'addresses', ['zipcode'], unique=True
	)


def downgrade() -> None:
	"""Drop address, state and city tables."""
	op.drop_index(op.f('ix_addresses_zipcode'), table_name='addresses')
	op.drop_index(op.f('ix_states_acronym'), table_name='states')
	op.drop_index(op.f('ix_cities_ibge'), table_name='cities')
	op.drop_table('addresses')
	op.drop_table('states')
	op.drop_table('cities')
	op.execute('DROP TYPE public.stateacronym')
