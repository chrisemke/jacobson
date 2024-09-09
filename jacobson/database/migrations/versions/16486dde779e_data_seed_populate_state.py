"""
Jacobson is a self hosted zipcode API
Copyright (C) 2023-2024 Christian G. Semke.

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
from uuid import uuid4

from alembic import op

from jacobson.database.models.brazil import State

"""
Data Seed: Populate State.

Revision ID: 16486dde779e
Revises: e5e1bdc106c3
Create Date: 2024-07-24 18:07:58.679658

"""

# revision identifiers, used by Alembic.
revision: str = '16486dde779e'
down_revision: str | None = 'e5e1bdc106c3'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	"""Insert all 27 states."""
	op.bulk_insert(
		State.__table__,  # type: ignore[attr-defined]
		[
			{'id': uuid4(), 'acronym': 'AC', 'name': 'Acre'},
			{'id': uuid4(), 'acronym': 'AL', 'name': 'Alagoas'},
			{'id': uuid4(), 'acronym': 'AP', 'name': 'Amapá'},
			{'id': uuid4(), 'acronym': 'AM', 'name': 'Amazonas'},
			{'id': uuid4(), 'acronym': 'BA', 'name': 'Bahia'},
			{'id': uuid4(), 'acronym': 'CE', 'name': 'Ceará'},
			{'id': uuid4(), 'acronym': 'DF', 'name': 'Distrito Federal'},
			{'id': uuid4(), 'acronym': 'ES', 'name': 'Espírito Santo'},
			{'id': uuid4(), 'acronym': 'GO', 'name': 'Goiás'},
			{'id': uuid4(), 'acronym': 'MA', 'name': 'Maranhão'},
			{'id': uuid4(), 'acronym': 'MT', 'name': 'Mato Grosso'},
			{'id': uuid4(), 'acronym': 'MS', 'name': 'Mato Grosso do Sul'},
			{'id': uuid4(), 'acronym': 'MG', 'name': 'Minas Gerais'},
			{'id': uuid4(), 'acronym': 'PA', 'name': 'Pará'},
			{'id': uuid4(), 'acronym': 'PB', 'name': 'Paraíba'},
			{'id': uuid4(), 'acronym': 'PR', 'name': 'Paraná'},
			{'id': uuid4(), 'acronym': 'PE', 'name': 'Pernambuco'},
			{'id': uuid4(), 'acronym': 'PI', 'name': 'Piauí'},
			{'id': uuid4(), 'acronym': 'RJ', 'name': 'Rio de Janeiro'},
			{'id': uuid4(), 'acronym': 'RN', 'name': 'Rio Grande do Norte'},
			{'id': uuid4(), 'acronym': 'RS', 'name': 'Rio Grande do Sul'},
			{'id': uuid4(), 'acronym': 'RO', 'name': 'Rondônia'},
			{'id': uuid4(), 'acronym': 'RR', 'name': 'Roraima'},
			{'id': uuid4(), 'acronym': 'SC', 'name': 'Santa Catarina'},
			{'id': uuid4(), 'acronym': 'SP', 'name': 'São Paulo'},
			{'id': uuid4(), 'acronym': 'SE', 'name': 'Sergipe'},
			{'id': uuid4(), 'acronym': 'TO', 'name': 'Tocantins'},
		],
	)


def downgrade() -> None:
	"""Remove all 27 states."""
	states = (
		"'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', "
		"'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', "
		"'RR', 'SC', 'SP', 'SE', 'TO'"
	)
	op.execute(f'DELETE FROM states WHERE acronym in ({states})')
