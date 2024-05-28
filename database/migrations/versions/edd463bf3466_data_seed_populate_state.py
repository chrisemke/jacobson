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

from alembic import op

from database.models.brazil import State

"""
Data Seed: Populate State.

Revision ID: edd463bf3466
Revises: c13b281db692
Create Date: 2024-05-25 00:13:00.151240

"""

# revision identifiers, used by Alembic.
revision: str = 'edd463bf3466'
down_revision: str | None = 'c13b281db692'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Insert all 27 states."""
    op.bulk_insert(
        State.__table__,  # type: ignore
        [
            {'id': 1, 'acronym': 'AC', 'name': 'Acre'},
            {'id': 2, 'acronym': 'AL', 'name': 'Alagoas'},
            {'id': 3, 'acronym': 'AP', 'name': 'Amapá'},
            {'id': 4, 'acronym': 'AM', 'name': 'Amazonas'},
            {'id': 5, 'acronym': 'BA', 'name': 'Bahia'},
            {'id': 6, 'acronym': 'CE', 'name': 'Ceará'},
            {'id': 7, 'acronym': 'DF', 'name': 'Distrito Federal'},
            {'id': 8, 'acronym': 'ES', 'name': 'Espírito Santo'},
            {'id': 9, 'acronym': 'GO', 'name': 'Goiás'},
            {'id': 10, 'acronym': 'MA', 'name': 'Maranhão'},
            {'id': 11, 'acronym': 'MT', 'name': 'Mato Grosso'},
            {'id': 12, 'acronym': 'MS', 'name': 'Mato Grosso do Sul'},
            {'id': 13, 'acronym': 'MG', 'name': 'Minas Gerais'},
            {'id': 14, 'acronym': 'PA', 'name': 'Pará'},
            {'id': 15, 'acronym': 'PB', 'name': 'Paraíba'},
            {'id': 16, 'acronym': 'PR', 'name': 'Paraná'},
            {'id': 17, 'acronym': 'PE', 'name': 'Pernambuco'},
            {'id': 18, 'acronym': 'PI', 'name': 'Piauí'},
            {'id': 19, 'acronym': 'RJ', 'name': 'Rio de Janeiro'},
            {'id': 20, 'acronym': 'RN', 'name': 'Rio Grande do Norte'},
            {'id': 21, 'acronym': 'RS', 'name': 'Rio Grande do Sul'},
            {'id': 22, 'acronym': 'RO', 'name': 'Rondônia'},
            {'id': 23, 'acronym': 'RR', 'name': 'Roraima'},
            {'id': 24, 'acronym': 'SC', 'name': 'Santa Catarina'},
            {'id': 25, 'acronym': 'SP', 'name': 'São Paulo'},
            {'id': 26, 'acronym': 'SE', 'name': 'Sergipe'},
            {'id': 27, 'acronym': 'TO', 'name': 'Tocantins'},
        ],
    )


def downgrade() -> None:
    """Remove all 27 states."""
    op.execute('DELETE FROM state WHERE id BETWEEN 1 AND 27')
