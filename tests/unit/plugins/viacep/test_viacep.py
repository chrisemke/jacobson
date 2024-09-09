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

from re import escape
from typing import Self

import pytest
from httpx import HTTPStatusError, Response
from respx import MockRouter

from jacobson.database.models.brazil import (
	Address,
	City,
	StateAcronym,
	StateCreate,
)
from jacobson.plugins.viacep.viacep import ViaCep


class TestViaCep:
	__slots__ = ('_ADDRESS_MOCK',)

	def setup_method(self: Self):
		self._ADDRESS_MOCK = {
			'cep': '01001-000',
			'logradouro': 'Praça da Sé',
			'complemento': 'lado ímpar',
			'bairro': 'Sé',
			'localidade': 'São Paulo',
			'uf': 'SP',
			'ibge': '3550308',
			'gia': '1004',
			'ddd': '11',
			'siafi': '7107',
		}

	async def test_get_address_by_zipcode_method_url_is_correct(
		self: Self, respx_mock: MockRouter
	) -> None:
		zipcode = 1001000
		mock = respx_mock.get(f'https://viacep.com.br/ws/{zipcode:08}/json/').mock(
			return_value=Response(200, json=self._ADDRESS_MOCK)
		)

		await ViaCep().get_address_by_zipcode(zipcode)

		assert mock.called

	async def test_get_address_by_zipcode_method_request_error(
		self: Self, respx_mock: MockRouter
	) -> None:
		zipcode = 1001000
		respx_mock.get(f'https://viacep.com.br/ws/{zipcode:08}/json/').mock(
			return_value=Response(
				400,
			)
		)

		with pytest.raises(
			HTTPStatusError,
			match=escape(
				"Client error '400 Bad Request' for url 'https://viacep.com.br/ws/01001000/json/'\n"
				'For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400'
			),
		):
			await ViaCep().get_address_by_zipcode(zipcode)

	async def test_get_address_by_zipcode_method_returns_address(
		self: Self, respx_mock: MockRouter
	) -> None:
		zipcode = 1001000
		respx_mock.get(f'https://viacep.com.br/ws/{zipcode:08}/json/').mock(
			return_value=Response(
				200,
				json=self._ADDRESS_MOCK,
			)
		)
		response = await ViaCep().get_address_by_zipcode(zipcode)

		assert response['data'][0].state == StateCreate(
			acronym=StateAcronym.SP, name='São Paulo', id=None
		)
		city_response_model = response['data'][0].city.model_dump()
		city_model = City(
			ibge=3550308, name='São Paulo', ddd=11, id=None
		).model_dump()
		city_model['id'] = city_response_model['id']
		assert city_response_model == city_model
		address_response_model = response['data'][0].model_dump()
		address_model = Address(
			zipcode=1001000,
			neighborhood='Sé',
			complement='Praça da Sé lado ímpar',
		).model_dump()
		address_model['id'] = address_response_model['id']
		address_model['updated_at'] = address_response_model['updated_at']
		assert address_response_model == address_model
