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

from http import HTTPStatus
from typing import Self

from httpx import AsyncClient

from database.models.brazil import City
from tests.integration.factories import AddressFactory


class TestMutation:
	async def test_create_address_success(
		self: Self, client: AsyncClient, city: City
	):
		address = AddressFactory()
		state = address.state.model_dump()
		state.pop('id')
		state['acronym'] = state['acronym'].value

		city = city.model_dump()
		city.pop('id')

		address = address.model_dump()
		address.pop('id')
		address.pop('updated_at')
		address['state'] = state
		address['city'] = city

		mutation = """
			mutation TestMutation($address: AddressInsertInput!) {
				createAddress(address: $address) {
					city {
						name
						ibge
						ddd
					}
					neighborhood
					complement
					zipcode
					state {
						name
						acronym
					}
					coordinates
				}
			}
		"""

		variables = {'address': address}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestMutation',
			},
		)

		assert response.status_code == HTTPStatus.OK
		assert response.json() == {'data': {'createAddress': address}}
