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

from typing import ClassVar, Self

from api.address.inputs import AddressFilterInput, AddressInsertInput
from api.address.types import AddressType
from api.schema import Mutation, Query
from database.models.brazil import (
	Address,
	City,
	CityCreate,
	State,
	StateCreate,
	StateAcronym,
)


class TestQuery:
	async def test_all_address(self: Self, mocker):
		state = State(acronym=StateAcronym.SP, name='São Paulo', id=None)
		city = City(ibge=3550308, name='São Paulo', ddd=11, id=None)
		address = Address(
			zipcode=1001000,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
			id=None,
			state=state,
			city=city,
		)

		class Session:
			session = ''

		class Info:
			context = Session()

		mocker.patch(
			'api.schema.get_address',
			return_value={'data': [address], 'provider': 'local'},
		)
		out = await Query().all_address(Info(), AddressFilterInput())
		address_model = address.model_dump()
		for i in out:
			assert isinstance(i, AddressType)
			address_response_model = i.to_pydantic().model_dump()
			address_model['id'] = address_response_model['id']
			address_model['updated_at'] = address_response_model['updated_at']

			assert address_response_model == address_model


class TestMutation:
	async def test_create_address(self: Self, mocker):
		state = StateCreate(acronym=StateAcronym.SP, name='São Paulo')
		city = CityCreate(ibge=3550308, name='São Paulo', ddd=11)
		address = AddressInsertInput(
			zipcode=1001000,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
			state=state,
			city=city,
		)

		class Session:
			session = ''

		class Info:
			context = Session()

		mocker.patch('api.schema.insert_address', return_value=address.to_pydantic())
		out = await Mutation().create_address(Info(), address)

		assert isinstance(out, AddressType)
		address_response_model = out.to_pydantic().model_dump()
		address_model = address.to_pydantic().model_dump()
		address_model['id'] = address_response_model['id']
		address_model['updated_at'] = address_response_model['updated_at']

		assert address_response_model == address_model
