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

from enum import StrEnum

# from typing import NamedTuple
from pydantic import PositiveInt
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)
from strawberry import enum


@enum
class StateAcronym(StrEnum):
    AC = 'AC'
    AL = 'AL'
    AP = 'AP'
    AM = 'AM'
    BA = 'BA'
    CE = 'CE'
    DF = 'DF'
    ES = 'ES'
    GO = 'GO'
    MA = 'MA'
    MT = 'MT'
    MS = 'MS'
    MG = 'MG'
    PA = 'PA'
    PB = 'PB'
    PR = 'PR'
    PE = 'PE'
    PI = 'PI'
    RJ = 'RJ'
    RN = 'RN'
    RS = 'RS'
    RO = 'RO'
    RR = 'RR'
    SC = 'SC'
    SP = 'SP'
    SE = 'SE'
    TO = 'TO'


class StateAcronymName(StrEnum):
    AC = 'Acre'
    AL = 'Alagoas'
    AP = 'Amapá'
    AM = 'Amazonas'
    BA = 'Bahia'
    CE = 'Ceará'
    DF = 'Distrito Federal'
    ES = 'Espírito Santo'
    GO = 'Goiás'
    MA = 'Maranhão'
    MT = 'Mato Grosso'
    MS = 'Mato Grosso do Sul'
    MG = 'Minas Gerais'
    PA = 'Pará'
    PB = 'Paraíba'
    PR = 'Paraná'
    PE = 'Pernambuco'
    PI = 'Piauí'
    RJ = 'Rio de Janeiro'
    RN = 'Rio Grande do Norte'
    RS = 'Rio Grande do Sul'
    RO = 'Rondônia'
    RR = 'Roraima'
    SC = 'Santa Catarina'
    SP = 'São Paulo'
    SE = 'Sergipe'
    TO = 'Tocantins'


class State(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    acronym: StateAcronym = Field(unique=True)
    name: str

    addresses: list['Address'] = Relationship(back_populates='state')


class City(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ibge: PositiveInt = Field(unique=True)
    name: str
    ddd: int | None = None

    addresses: list['Address'] = Relationship(back_populates='city')


# class Coordinates(NamedTuple):
#     latitude: float
#     longitude: float
#     altitude: float


# Needed until strawberry support auto | None type
# https://github.com/strawberry-graphql/strawberry/issues/3435
class AddressBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    zipcode: int | None = Field(None, gt=1_000_000, lt=99_999_999)
    neighborhood: str | None = None
    complement: str | None = None
    # coordinates: Coordinates | None = None


class Address(AddressBase, table=True):
    zipcode: int = Field(unique=True, gt=1_000_000, lt=99_999_999)

    state_id: PositiveInt = Field(foreign_key='state.id')
    state: State = Relationship(back_populates='addresses')

    city_id: PositiveInt = Field(foreign_key='city.id')
    city: City = Relationship(back_populates='addresses')

    neighborhood: str
    complement: str | None = None
