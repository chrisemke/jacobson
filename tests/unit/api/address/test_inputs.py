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

from api.address.graphql_inputs import (
	AddressFilterInput,
	AddressInsertInput,
	CityInput,
	StateInput,
)
from database.models.brazil import StateAcronym


class TestInputs:
	def test_state_input(self: Self):
		state_input = StateInput(name='São Paulo', acronym=StateAcronym.SP)

		assert state_input.__dict__ == {
			'acronym': StateAcronym.SP,
			'name': 'São Paulo',
		}

	def test_state_input_no_name(self: Self):
		state_input = StateInput(name=None, acronym=StateAcronym.SP)
		assert state_input.name is None

	def test_city_input(self: Self):
		city_input = CityInput(ibge=3550308, name='São Paulo', ddd=11)
		assert city_input.__dict__ == {
			'ibge': 3550308,
			'name': 'São Paulo',
			'ddd': 11,
		}

	def test_city_input_no_name(self: Self):
		city_input = CityInput(ibge=3550308, name=None, ddd=11)
		assert city_input.name is None

	def test_address_filter_input(self: Self):
		state_input = StateInput(name='São Paulo', acronym=StateAcronym.SP)
		city_input = CityInput(ibge=3550308, name='São Paulo', ddd=11)
		address_filter_input = AddressFilterInput(
			zipcode=1001000,
			city=city_input,
			state=state_input,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
		)

		assert address_filter_input.__dict__ == {
			'zipcode': 1001000,
			'neighborhood': 'Sé',
			'complement': 'Praça da Sé - lado ímpar',
			'coordinates': None,
			'state': state_input,
			'city': city_input,
		}

	def test_address_filter_input_no_city_or_state(self: Self):
		address_filter_input = AddressFilterInput(
			zipcode=1001000,
			city=None,
			state=None,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
		)
		assert address_filter_input.__dict__ == {
			'zipcode': 1001000,
			'neighborhood': 'Sé',
			'complement': 'Praça da Sé - lado ímpar',
			'coordinates': None,
			'state': None,
			'city': None,
		}

	def test_address_insert_input(self: Self):
		state_input = StateInput(name=None, acronym=StateAcronym.SP)
		city_input = CityInput(ibge=3550308, name='São Paulo', ddd=11)
		address_insert_input = AddressInsertInput(
			zipcode=1001000,
			city=city_input,
			state=state_input,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
		)

		assert address_insert_input.__dict__ == {
			'zipcode': 1001000,
			'neighborhood': 'Sé',
			'complement': 'Praça da Sé - lado ímpar',
			'coordinates': None,
			'state': state_input,
			'city': city_input,
		}
