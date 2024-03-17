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

from enum import Enum

from strawberry import auto, enum, type
from strawberry.experimental.pydantic import type as pydantic_type

from api.models import Address, City, State


@enum
class StateAcronym(Enum):
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


@pydantic_type(name='State', model=State)
class StateType:
    name: auto
    acronym: StateAcronym


@pydantic_type(name='City', model=City)
class CityType:
    ibge: auto
    name: auto


@type(name='Coords')
class CoordsType:
    """A coordinate consists latitude, longitude and altitude."""

    latitude: float
    longitude: float
    altitude: float


@pydantic_type(name='Address', model=Address)
class AddressType:
    zipcode: auto
    city: auto
    state: auto
    district: auto
    complement: auto
    neighborhood: auto
    coords: CoordsType | None = None
