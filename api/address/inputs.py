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

from strawberry import auto, input
from strawberry.experimental.pydantic import input as pydantic_input

from database.models.brazil import AddressBase, City, State


@pydantic_input(model=State)
class StateInput:
    name: auto
    acronym: auto


@pydantic_input(model=City)
class CityInput:
    ibge: auto
    name: auto
    ddd: auto


@input
class CoordinatesInput:
    latitude: float
    longitude: float
    altitude: float | None = None


@pydantic_input(model=AddressBase)
class AddressInput:
    zipcode: auto
    city: CityInput | None = None
    state: StateInput | None = None
    neighborhood: auto
    complement: auto
    # coordinates: CoordinatesInput | None = None
