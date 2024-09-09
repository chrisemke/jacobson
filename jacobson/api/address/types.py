"""
Jacobson is a self hosted zipcode API
Copyright (C) 2023-2024 Christian G. Semke.

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

from typing import TypedDict

from strawberry import auto
from strawberry.experimental.pydantic import type as pydantic_type
from strawberry.scalars import JSON

from jacobson.database.models.brazil import (
	Address,
	CityCreate,
	StateCreate,
)


@pydantic_type(StateCreate, name='State')
class StateType:
	name: auto
	acronym: auto


@pydantic_type(CityCreate, name='City')
class CityType:
	ibge: auto
	name: auto
	ddd: auto


@pydantic_type(Address, name='Address')
class AddressType:
	zipcode: auto
	city: CityType
	state: StateType
	neighborhood: auto
	complement: auto
	coordinates: JSON | None = None


class DictResponse(TypedDict):
	data: list[Address]
	provider: str
