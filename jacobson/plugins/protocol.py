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

from abc import abstractmethod
from typing import Protocol, Self, runtime_checkable

from pydantic import PositiveInt

from jacobson.api.address.types import DictResponse


@runtime_checkable
class Plugin(Protocol):
	@abstractmethod
	async def get_address_by_zipcode(
		self: Self, zipcode: PositiveInt
	) -> DictResponse:
		"""Get address by zipcode."""
