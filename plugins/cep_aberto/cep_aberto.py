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
from utils.settings import settings


class CepAbertoState(TypedDict):
    sigla: str


class CepAbertoCity(TypedDict):
    ddd: int
    ibge: str
    nome: str


class CepAbertoAddress(TypedDict):
    altitude: float
    cep: str
    latitude: str
    longitude: str
    logradouro: str
    bairro: str
    complemento: str
    cidade: CepAbertoCity
    estado: CepAbertoState


class CepAberto:
    __slots__ = ('token',)

    def __init__(self: Self) -> None:
        """
        Set token attribute.

        Parameters
        ----------
        self : Self
            scope of current class

        Raises
        ------
        Exception
            if token does not exists.

        Todo:
        ____
        - Fix generic exception

        """
        if not settings.CEP_ABERTO_TOKEN:
            raise Exception('Token Inválido')
        self.token = settings.CEP_ABERTO_TOKEN

    async def get_address_by_zipcode(
        self: Self, zipcode: PositiveInt
    ) -> list[Address]:
        """
        Get address by zipcode using Cep Aberto API.

        Parameters
        ----------
        self : Self
            scope of the CepAberto class
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
        url = f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
        headers = {'Authorization': f'Token token={self.token}'}
        request = get(url, headers=headers)

        if request.status_code != 200:
            raise Exception('Something went wrong, request status code != 200')

        return [await self._request_to_database_model(request.json())]

    @classmethod
    async def _request_to_database_model(
        cls, address_data: CepAbertoAddress
    ) -> Address:
        """
        Receive a json/dict and return an Address object.

        Parameters
        ----------
        address_data : CepAbertoAddress
            here's a dict example
            {
                "altitude":760.0,
                "cep":"01001000",
                "latitude":"-23.5479099981",
                "longitude":"-46.636",
                "logradouro":"Praça da Sé",
                "bairro":"Sé",
                "complemento":"- lado ímpar",
                "cidade":{
                    "ddd":11,
                    "ibge":"3550308",
                    "nome":"São Paulo"
                },
                "estado":{
                    "sigla":"SP"
                }
            }

        Returns
        -------
        Address
            The Database model from database.models.brazil

        """
        acronym = address_data['estado']['sigla']
        state = State(
            acronym=StateAcronym(acronym),
            name=getattr(StateAcronymName, acronym).value,
        )

        city = City(
            ibge=int(address_data['cidade']['ibge']),
            name=address_data['cidade']['nome'],
            ddd=address_data['cidade']['ddd'],
        )
        logradouro = None
        if address_data['logradouro']:
            logradouro = (
                f'{address_data['logradouro']} {address_data['complemento']}'
            ).strip()

        return Address(
            zipcode=int(address_data['cep']),
            state=state,
            city=city,
            neighborhood=address_data['bairro'],
            complement=logradouro,
        )
