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

from uuid import uuid4

from pydantic import UUID4, EmailStr, model_validator
from sqlmodel import (
	Field,
	SQLModel,
)


class UserBase(SQLModel):
	email: EmailStr | None = None
	username: str | None = None


class UserLogin(UserBase):
	email: EmailStr | None = None
	username: str | None = None
	password: str

	@model_validator(mode='before')
	@classmethod
	def verificar_atributos(
		cls, values: dict[str, str | None]
	) -> dict[str, str | None]:
		"""
		Check if email or username have any value.

		Args:
				values (dict[str, str  |  None]): dict of attributes in the class

		Raises:
				ValueError: if email and username are None

		Returns:
				dict[str, str | None]: decame dict of attributes in the class

		"""
		if not values.get('email') and not values.get('username'):
			raise ValueError('User MUST have one of the attributes user or email')
		return values


class User(UserLogin, table=True):
	__tablename__ = 'users'

	id: UUID4 | None = Field(default_factory=uuid4, primary_key=True)

	email: EmailStr = Field(
		unique=True,
		index=True,
		nullable=False,
	)
	username: str
