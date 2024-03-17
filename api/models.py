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
from typing import NamedTuple

from pydantic import BaseModel, PositiveInt


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


class State(BaseModel):
    name: str
    acronym: StateAcronym


class City(BaseModel):
    ibge: PositiveInt
    name: str


class Coords(NamedTuple):
    """A coordinate consists latitude, longitude and altitude."""

    latitude: float
    longitude: float
    altitude: float


class Address(BaseModel):
    zipcode: PositiveInt
    city: City
    state: State
    district: str | None = None
    complement: str
    neighborhood: str
    coords: Coords | None = None


class OptionalAddress(BaseModel):
    zipcode: PositiveInt | None = None
    city: City | None = None
    state: State | None = None
    district: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    coords: Coords | None = None
