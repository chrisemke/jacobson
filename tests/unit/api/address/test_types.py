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

from typing import Self

from api.address.types import AddressType, CityType, StateType
from database.models.brazil import StateAcronym


class TestTypes:
	def test_state_type(self: Self):
		state_input = StateType(name='São Paulo', acronym=StateAcronym.SP)
		assert state_input.to_pydantic().model_dump() == {
			'acronym': StateAcronym.SP,
			'name': 'São Paulo',
		}

	def test_city_type(self: Self):
		city_input = CityType(ibge=3550308, name='São Paulo', ddd=11)
		assert city_input.to_pydantic().model_dump() == {
			'ibge': 3550308,
			'name': 'São Paulo',
			'ddd': 11,
		}

	def test_address_type(self: Self):
		state_input = StateType(name='São Paulo', acronym=StateAcronym.SP)
		city_input = CityType(ibge=3550308, name='São Paulo', ddd=11)
		address_filter_input = AddressType(
			zipcode=1001000,
			city=city_input,
			state=state_input,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
		)
		address_model = address_filter_input.to_pydantic().model_dump()

		assert address_model == {
			'zipcode': 1001000,
			'neighborhood': 'Sé',
			'complement': 'Praça da Sé - lado ímpar',
			'coordinates': None,
			'id': address_model['id'],
			'updated_at': address_model['updated_at'],
		}
		assert address_filter_input.state == state_input
		assert address_filter_input.city == city_input
