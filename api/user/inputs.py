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

from strawberry import auto
from strawberry.experimental.pydantic import input as pydantic_input

from database.models.user import User, UserLogin


@pydantic_input(User)
class UserRegisterInput:
	email: auto
	username: auto
	password: auto


@pydantic_input(UserLogin)
class LoginInput:
	email: auto
	username: auto
	password: auto
