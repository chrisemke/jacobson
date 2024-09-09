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

from dataclasses import dataclass
from re import escape
from typing import Self

import pytest
from httpx import HTTPStatusError, Response
from pytest_mock import MockerFixture
from respx import MockRouter

from jacobson.database.models.brazil import (
	Address,
	City,
	StateAcronym,
	StateCreate,
)
from jacobson.plugins.cep_aberto.cep_aberto import CepAberto


@dataclass
class SettingsMock:
	CEP_ABERTO_TOKEN: str | None = 'valid_token'


class TestCepAberto:
	__slots__ = ('_ADDRESS_MOCK',)

	def setup_method(self: Self):
		self._ADDRESS_MOCK = {
			'altitude': 760.0,
			'cep': '01001000',
			'latitude': '-23.5479099981',
			'longitude': '-46.636',
			'logradouro': 'Praça da Sé',
			'bairro': 'Sé',
			'complemento': '- lado ímpar',
			'cidade': {
				'ddd': 11,
				'ibge': '3550308',
				'nome': 'São Paulo',
			},
			'estado': {'sigla': 'SP'},
		}

	def test_valid_token(self: Self, mocker: MockerFixture) -> None:
		mocker.patch('jacobson.plugins.cep_aberto.cep_aberto.settings', SettingsMock)
		assert CepAberto().token == 'valid_token'

	def test_invalid_token(self: Self, mocker: MockerFixture) -> None:
		mocker.patch(
			'jacobson.plugins.cep_aberto.cep_aberto.settings',
			SettingsMock(CEP_ABERTO_TOKEN=None),
		)

		with pytest.raises(Exception, match='Token Inválido'):
			CepAberto()

	async def test_get_address_by_zipcode_method_url_is_correct(
		self: Self, mocker: MockerFixture, respx_mock: MockRouter
	) -> None:
		mocker.patch('jacobson.plugins.cep_aberto.cep_aberto.settings', SettingsMock)

		zipcode = 1001000
		mock = respx_mock.get(
			f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
		).mock(return_value=Response(200, json=self._ADDRESS_MOCK))

		await CepAberto().get_address_by_zipcode(zipcode)

		assert mock.called

	async def test_get_address_by_zipcode_method_headers_are_correct(
		self: Self, mocker: MockerFixture, respx_mock: MockRouter
	) -> None:
		mocker.patch('jacobson.plugins.cep_aberto.cep_aberto.settings', SettingsMock)

		zipcode = 1001000
		respx_mock.get(
			f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}',
			headers={
				'Authorization': f'Token token={SettingsMock.CEP_ABERTO_TOKEN}',
			},
		).mock(return_value=Response(200, json=self._ADDRESS_MOCK))

		await CepAberto().get_address_by_zipcode(zipcode)

	async def test_get_address_by_zipcode_method_request_error(
		self: Self, mocker: MockerFixture, respx_mock: MockRouter
	) -> None:
		mocker.patch('jacobson.plugins.cep_aberto.cep_aberto.settings', SettingsMock)

		zipcode = 1001000
		respx_mock.get(
			f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
		).mock(
			return_value=Response(
				400,
			)
		)

		with pytest.raises(
			HTTPStatusError,
			match=escape(
				"Client error '400 Bad Request' for url 'https://www.cepaberto.com/api/v3/cep?cep=01001000'\n"
				'For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400'
			),
		):
			await CepAberto().get_address_by_zipcode(zipcode)

	async def test_get_address_by_zipcode_method_returns_address(
		self: Self, mocker: MockerFixture, respx_mock: MockRouter
	) -> None:
		mocker.patch('jacobson.plugins.cep_aberto.cep_aberto.settings', SettingsMock)

		zipcode = 1001000
		respx_mock.get(
			f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
		).mock(
			return_value=Response(
				200,
				json=self._ADDRESS_MOCK,
			)
		)
		response = await CepAberto().get_address_by_zipcode(zipcode)

		assert response['data'][0].state == StateCreate(
			acronym=StateAcronym.SP, name='São Paulo', id=None
		)
		city_response_model = response['data'][0].city.model_dump()
		city_model = City(
			ibge=3550308, name='São Paulo', ddd=11, id=None
		).model_dump()
		city_model['id'] = city_response_model['id']
		assert city_response_model == city_model
		response_model = response['data'][0].model_dump()
		address_model = Address(
			zipcode=1001000,
			neighborhood='Sé',
			complement='Praça da Sé - lado ímpar',
			coordinates={
				'altitude': 760.0,
				'latitude': -23.5479099981,
				'longitude': -46.636,
			},
		).model_dump()
		address_model['id'] = response_model['id']
		address_model['updated_at'] = response_model['updated_at']
		assert response_model == address_model
