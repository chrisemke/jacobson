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

from typing import Self, TypedDict

from httpx import get
from pydantic import PositiveInt

from database.models.brazil import (
    Address,
    City,
    State,
    StateAcronym,
    StateAcronymName,
)
from plugins.protocol import Plugin


class ViaCepAddress(TypedDict):
    cep: str
    logradouro: str
    complemento: str
    bairro: str
    localidade: str
    uf: str
    ibge: str
    gia: str
    ddd: str
    siafi: str


class ViaCep(Plugin):
    async def get_address_by_zipcode(
        self: Self, zipcode: PositiveInt
    ) -> list[Address]:
        """
        Get address by zipcode.

        Parameters
        ----------
        self : Self
            scope of the class
        zipcode : PositiveInt
            Zipcode to search for, it should be > 1_000_000 and < 99_999_999

        Returns
        -------
        list[Address]
            A valid address or exception

        Raises
        ------
        Exception
            If the request went wrong or it does not return any data

        Todo:
        ____
        - Fix generic exception

        """
        request = get(f'https://viacep.com.br/ws/{zipcode:08}/json/')

        if request.status_code != 200:
            raise Exception('Something went wrong, request status code != 200')

        return [await self._request_to_database_model(request.json())]

    @classmethod
    async def _request_to_database_model(
        cls, address_data: ViaCepAddress
    ) -> Address:
        """
        Receive a json/dict and return an Address object.

        Parameters
        ----------
        address_data : ViaCepAddress
            here's a dict example
            {
                "cep": "01001-000",
                "logradouro": "Praça da Sé",
                "complemento": "lado ímpar",
                "bairro": "Sé",
                "localidade": "São Paulo",
                "uf": "SP",
                "ibge": "3550308",
                "gia": "1004",
                "ddd": "11",
                "siafi": "7107"
            }

        Returns
        -------
        Address
            The Database model from database.models.brazil

        """
        acronym = address_data['uf']
        state = State(
            acronym=StateAcronym(acronym),
            name=getattr(StateAcronymName, acronym).value,
        )

        city = City(
            ibge=int(address_data['ibge']),
            name=address_data['localidade'],
            ddd=int(address_data['ddd']),
        )
        logradouro = None
        if address_data['logradouro']:
            logradouro = (
                f'{address_data['logradouro']} {address_data['complemento']}'
            ).strip()

        return Address(
            zipcode=int(address_data['cep'].replace('-', '')),
            state=state,
            city=city,
            neighborhood=address_data['bairro'],
            complement=logradouro,
        )
