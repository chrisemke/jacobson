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

from typing import Annotated, Self

from fastapi import Depends
from pydantic import PositiveInt
from sqlmodel.ext.asyncio.session import AsyncSession
from strawberry import Info, Schema, field, type
from strawberry.fastapi import BaseContext, GraphQLRouter

from api.address.graphql_inputs import AddressFilterInput, AddressInsertInput
from api.address.graphql_types import AddressType
from api.resolvers import get_address, insert_address
from database import functions
from database.engine import get_session
from utils.settings import settings


@type
class Query:
	@field
	async def all_address(
		self: Self,
		info: Info,
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
				functions.insert_address, info.context.session, result['data'][0]
			)
			# insert log

		return list(
			map(
				AddressType.from_pydantic,
				result['data'],
			)
		)


@type
class Mutation:
	@field
	async def create_address(
		self: Self, info: Info, address: AddressInsertInput
	) -> AddressType:
		"""
		Insert address and city if not exists on database.

		Args:
				info (Info): Strawberry default value to get context information
						in this case we use 'db'
				address (AddressInsertInput): Strict address class,
						almost all fields need to be passed

		Returns:
				AddressType: Address (db model converted to strawberry dataclass)

		"""
		return AddressType.from_pydantic(
			await insert_address(info.context.session, address)
		)


class CustomContext(BaseContext):
	def __init__(self: Self, session: AsyncSession):
		"""Generate context database session."""
		self.session = session


async def get_context(
	session: Annotated[AsyncSession, Depends(get_session)],
) -> CustomContext:
	"""
	Create database session to use when needed.

	Args:
			session (Annotated[AsyncSession, Depends): get db session from get_session

	Returns:
			CustomContext: class that contains db session

	"""
	return CustomContext(session)


schema = Schema(query=Query, mutation=Mutation)

"""Create Graphql Router for fastapi and start graphql ide if env is DEV."""
graphql_app = GraphQLRouter[object, object](
	schema,
	context_getter=get_context,
	graphql_ide='graphiql' if settings.DEV else None,
)
