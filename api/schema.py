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

from http import HTTPStatus
from typing import Self

from fastapi import Depends, HTTPException
from pydantic import PositiveInt
from strawberry import Info, Schema, field, mutation, type
from strawberry.fastapi import GraphQLRouter

from api.address.inputs import AddressFilterInput, AddressInsertInput
from api.address.types import AddressType
from api.auth import AuthExtension
from api.context import Context
from api.resolvers import (
	authenticate_user,
	create_user,
	get_address,
	insert_address,
	insert_address_background,
	refresh_token_by_id,
)
from api.security import verify_password
from api.user.inputs import LoginInput, UserRegisterInput
from api.user.types import LoginType
from utils.settings import settings


@type
class Query:
	@field(extensions=[AuthExtension])  # type: ignore[misc]
	async def all_address(
		self: Self,
		info: Info[Context],
		filter: AddressFilterInput,
		page_size: PositiveInt = 10,
		page_number: PositiveInt = 1,
	) -> list[AddressType]:
		"""
		Query all addresses from database or all plugins.

		Args:
				info (Info): Strawberry default value to get context information
						in this case we use 'db'
				filter (AddressFilterInput): Strawberry input dataclass,
						everything can be None (based on sqlmodel model)
				page_size (PositiveInt, optional): How many elements in each page.
						Defaults to 10.
				page_number (PositiveInt, optional): Number of the page. Defaults to 1.

		Returns:
				list[AddressType]: All addresses (db model converted to strawberry type)
						based on filter or empty list

		"""
		result = await get_address(
			info.context.session, filter, page_size, page_number
		)
		if result['provider'] != 'local' and result['data']:
			info.context.background_tasks.add_task(
				insert_address_background, info.context.session, result['data'][0]
			)

		return list(
			map(
				AddressType.from_pydantic,
				result['data'],
			)
		)


@type
class Mutation:
	@mutation(extensions=[AuthExtension])  # type: ignore[misc]
	async def create_address(
		self: Self, info: Info[Context], address: AddressInsertInput
	) -> AddressType:
		"""
		Insert address and city if not exists on database.

		Args:
				info (Info[Context]): Strawberry default value to get context information
						in this case we use 'db'
				address (AddressInsertInput): Strict address class,
						almost all fields need to be passed

		Returns:
				AddressType: Address (db model converted to strawberry dataclass)

		"""
		return AddressType.from_pydantic(
			await insert_address(info.context.session, address)
		)

	@mutation(extensions=[AuthExtension])  # type: ignore[misc]
	async def refresh_token(self: Self, info: Info[Context]) -> str | None:
		"""
		Refresh jwt token.

		Args:
				self (Self): Scope of current class
				info (Info[Context]): Custom context, contains current user

		Returns:
				str: jwt token

		"""
		if user := await info.context.user():
			return await refresh_token_by_id(str(user.id))
		return None

	@mutation
	async def login(
		self: Self, info: Info[Context], login_data: LoginInput
	) -> LoginType:
		"""
		Authenticate user.

		Args:
				self (Self): Scope of current class
				info (Info[Context]): Custom context, contains db session
				login_data (LoginInput): Username | Email and password

		Returns:
				LoginType: Authenticated Login

		"""
		user = await authenticate_user(
			info.context.session, login_data.to_pydantic()
		)
		if not user or not verify_password(login_data.password, user.password):
			response = info.context.response

			response.status_code = HTTPStatus.UNAUTHORIZED
			response.headers['WWW-Authenticate'] = 'Bearer'
			raise HTTPException(
				status_code=HTTPStatus.UNAUTHORIZED,
				detail='Could not validate credentials',
				headers={'WWW-Authenticate': 'Bearer'},
			)

		return LoginType.from_pydantic(user)

	@mutation
	async def register(
		self: Self, info: Info[Context], register_data: UserRegisterInput
	) -> LoginType:
		"""
		Register user on database.

		Args:
				info (Info[Context]): Scope of current class
				register_data (UserRegisterInput): User data

		Returns:
				bool: True if succeed

		"""
		return LoginType.from_pydantic(
			await create_user(
				info.context.session, info.context.response, register_data
			)
		)


schema = Schema(query=Query, mutation=Mutation)

"""Create Graphql Router for fastapi and start graphql ide if env is DEV."""
graphql_app = GraphQLRouter[object, object](
	schema,
	context_getter=lambda context=Depends(Context): context,
	graphql_ide='graphiql' if settings.DEV else None,
)
