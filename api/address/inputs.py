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

from strawberry import auto, enum, input
from strawberry.experimental.pydantic import input as pydantic_input

from api.models import City, OptionalAddress, State


@enum
class StateAcronymInput(Enum):
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


@pydantic_input(model=State)
class StateInput:
    name: auto
    acronym: StateAcronymInput


@pydantic_input(model=City)
class CityInput:
    ibge: auto
    name: auto


@input
class CoordsInput:
    """A coordinate consists latitude, longitude and altitude."""

    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None


@pydantic_input(model=OptionalAddress)
class AddressInput:
    zipcode: auto
    city: auto
    state: auto
    district: auto
    complement: auto
    neighborhood: auto
    coords: CoordsInput | None = None
