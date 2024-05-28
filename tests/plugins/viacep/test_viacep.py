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

from httpx import Response
from pytest import mark, raises

from database.models.brazil import (
    Address,
    City,
    State,
    StateAcronym,
)
from plugins.viacep.viacep import ViaCep


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

    @mark.asyncio
    async def test_get_address_by_zipcode_method_url_is_correct(
        self: Self, respx_mock
    ) -> None:
        zipcode = 1001000
        mock = respx_mock.get(
            f'https://viacep.com.br/ws/{zipcode:08}/json/'
        ).mock(return_value=Response(200, json=self._ADDRESS_MOCK))

        await ViaCep().get_address_by_zipcode(zipcode)

        assert mock.called

    @mark.asyncio
    async def test_get_address_by_zipcode_method_request_error(
        self: Self, respx_mock
    ) -> None:
        zipcode = 1001000
        respx_mock.get(f'https://viacep.com.br/ws/{zipcode:08}/json/').mock(
            return_value=Response(
                400,
            )
        )

        with raises(
            Exception, match='Something went wrong, request status code != 200'
        ):
            await ViaCep().get_address_by_zipcode(zipcode)

    @mark.asyncio
    async def test_get_address_by_zipcode_method_returns_address(
        self: Self, respx_mock
    ) -> None:
        zipcode = 1001000
        respx_mock.get(
            f'https://viacep.com.br/ws/{zipcode:08}/json/'
        ).mock(
            return_value=Response(
                200,
                json=self._ADDRESS_MOCK,
            )
        )
        response = await ViaCep().get_address_by_zipcode(zipcode)

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
                complement='Praça da Sé lado ímpar',
                id=None,
            )
        ]
