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

from dataclasses import dataclass
from typing import Self

from httpx import Response
from pytest import mark, raises
from pytest_mock import MockerFixture

from database.models.brazil import (
    Address,
    City,
    State,
    StateAcronym,
)
from plugins.cep_aberto.cep_aberto import CepAberto


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
        mocker.patch('plugins.cep_aberto.cep_aberto.settings', SettingsMock)
        assert CepAberto().token == 'valid_token'

    def test_invalid_token(self: Self, mocker: MockerFixture) -> None:
        mocker.patch(
            'plugins.cep_aberto.cep_aberto.settings',
            SettingsMock(CEP_ABERTO_TOKEN=None),
        )

        with raises(Exception, match='Token Inválido'):
            CepAberto()

    @mark.asyncio
    async def test_get_address_by_zipcode_method_url_is_correct(
        self: Self, mocker: MockerFixture, respx_mock
    ) -> None:
        mocker.patch('plugins.cep_aberto.cep_aberto.settings', SettingsMock)

        zipcode = 1001000
        mock = respx_mock.get(
            f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
        ).mock(return_value=Response(200, json=self._ADDRESS_MOCK))

        await CepAberto().get_address_by_zipcode(zipcode)

        assert mock.called

    @mark.asyncio
    async def test_get_address_by_zipcode_method_headers_are_correct(
        self: Self, mocker: MockerFixture, respx_mock
    ) -> None:
        mocker.patch('plugins.cep_aberto.cep_aberto.settings', SettingsMock)

        zipcode = 1001000
        respx_mock.get(
            f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}',
            headers={
                'Authorization': f'Token token={SettingsMock.CEP_ABERTO_TOKEN}',
            },
        ).mock(return_value=Response(200, json=self._ADDRESS_MOCK))

        await CepAberto().get_address_by_zipcode(zipcode)

    @mark.asyncio
    async def test_get_address_by_zipcode_method_request_error(
        self: Self, mocker: MockerFixture, respx_mock
    ) -> None:
        mocker.patch('plugins.cep_aberto.cep_aberto.settings', SettingsMock)

        zipcode = 1001000
        respx_mock.get(
            f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
        ).mock(
            return_value=Response(
                400,
            )
        )

        with raises(
            Exception, match='Something went wrong, request status code != 200'
        ):
            await CepAberto().get_address_by_zipcode(zipcode)

    @mark.asyncio
    async def test_get_address_by_zipcode_method_returns_address(
        self: Self, mocker: MockerFixture, respx_mock
    ) -> None:
        mocker.patch('plugins.cep_aberto.cep_aberto.settings', SettingsMock)

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

        assert response[0].state == State(
            acronym=StateAcronym.SP, name='São Paulo', id=None
        )
        assert response[0].city == City(
            ibge=3550308, name='São Paulo', ddd=11, id=None
        )
        assert response == [
            Address(
                zipcode=1001000,
                neighborhood='Sé',
                complement='Praça da Sé - lado ímpar',
                id=None,
            )
        ]
