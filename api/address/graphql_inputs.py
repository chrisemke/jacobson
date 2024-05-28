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

from strawberry import auto
from strawberry.experimental.pydantic import input as pydantic_input

from database.models.brazil import Address, AddressBase, City, State


@pydantic_input(model=State)
class StateInput:
    acronym: auto
    # Needed until strawberry support auto | None type
    # https://github.com/strawberry-graphql/strawberry/issues/3435
    name: str | None = None


@pydantic_input(model=City)
class CityInput:
    ibge: auto
    # Needed until strawberry support auto | None type
    # https://github.com/strawberry-graphql/strawberry/issues/3435
    name: str | None = None
    ddd: auto


# @input
# class CoordinatesInput:
#     latitude: float
#     longitude: float
#     altitude: float | None = None


@pydantic_input(model=AddressBase)
class AddressFilterInput:
    zipcode: auto
    city: CityInput | None = None
    state: StateInput | None = None
    neighborhood: auto
    complement: auto
    # coordinates: CoordinatesInput | None = None


@pydantic_input(model=Address)
class AddressInsertInput:
    zipcode: auto
    state: StateInput
    city: CityInput
    neighborhood: auto
    complement: auto
