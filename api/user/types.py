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

from typing import Self

from strawberry import auto, field
from strawberry.experimental.pydantic import type as pydantic_type

from api.jwt.jwt_manager import create_access_token
from database.models.user import User


@pydantic_type(User)
class LoginType:
	id: auto
	email: auto
	username: auto

	@field
	def jwt(self: Self) -> str:
		"""
		Generate jwt token based on current id.

		Args:
				self (Self): Scope of current class

		Returns:
				str: Jwt token

		"""
		return create_access_token({'sub': str(self.id)})
