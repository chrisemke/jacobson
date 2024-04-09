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

from strawberry import auto, type
from strawberry.experimental.pydantic import type as pydantic_type

from database.models.brazil import Address, City, State


@pydantic_type(name='State', model=State)
class StateType:
    name: auto
    acronym: auto


@pydantic_type(name='City', model=City)
class CityType:
    ibge: auto
    name: auto
    ddd: auto


@type(name='Coordinates')
class CoordinatesType:
    latitude: float
    longitude: float
    altitude: float


@pydantic_type(name='Address', model=Address)
class AddressType:
    zipcode: auto
    city: CityType
    state: StateType
    neighborhood: auto
    complement: auto
    coordinates: CoordinatesType | None = None
