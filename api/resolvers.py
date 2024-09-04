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

from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import Response

from api.address.inputs import AddressFilterInput, AddressInsertInput
from api.address.types import DictResponse
from api.jwt.jwt_manager import create_access_token
from api.security import get_password_hash
from api.user.inputs import UserRegisterInput
from database.models.brazil import Address
from database.models.user import User, UserLogin
from database.repositories.brazil import BrazilRepository
from database.repositories.user import UserRepository
from plugins.plugins_controller import get_zipcode_from_plugins


async def get_address(
	session: AsyncSession,
	filter: AddressFilterInput,
	page_size: PositiveInt,
	page_number: PositiveInt,
) -> DictResponse:
	"""
	Get all addresses from database or all plugins.

	Args:
			session (AsyncSession): Database session
			filter (AddressFilterInput): Strawberry input dataclass,
					everything can be None (based on sqlmodel model)
			page_size (PositiveInt): How many elements in each page
			page_number (PositiveInt): Number of the page

	Returns:
			DictResponse: 'data' key has all addresses
					(db model) based on filter or empty list;
					'provider' key has the service provider local or some plugin

	"""
	result = await BrazilRepository.get_address_by_dc_join_state_join_city(
		session, filter, page_size, page_number
	)
	if result or not filter.zipcode:
		return {'data': result, 'provider': 'local'}

	return await get_zipcode_from_plugins(filter.zipcode)


async def insert_address(
	session: AsyncSession, address: AddressInsertInput
) -> Address:
	"""
	Insert address and city if not exists on database.

	Args:
			session (AsyncSession): Database session
			address (AddressInsertInput): Strict address class,
					all needed fields need to be passed

	Returns:
			Address: Address (db model)

	"""
	return await BrazilRepository.insert_address_by_dc(session, address)


async def insert_address_background(
	session: AsyncSession, address: Address
) -> None:
	"""
	Corrotine to insert address with no return.

	Args:
			session (AsyncSession): Database session
			address (Address): database model ready to insert

	"""
	await BrazilRepository.insert_address_background(session, address)


async def refresh_token_by_id(id: str) -> str:
	"""
	Refresh jwt token.

	Args:
			id (str): user uuid

	Returns:
			str: jwt token

	"""
	return create_access_token({'sub': id})


async def authenticate_user(
	session: AsyncSession, login_data: UserLogin
) -> User | None:
	"""
	Auth user based on email or username and password.

	Args:
			session (AsyncSession): Database session
			login_data (UserLogin): (email or username) and password is needed

	Returns:
			User: User DB model

	"""
	if login_data.email:
		return await UserRepository.get_user_by_email(session, login_data.email)
	if login_data.username:
		return await UserRepository.get_user_by_username(
			session, login_data.username
		)
	return None


async def create_user(
	session: AsyncSession, response: Response, register_data: UserRegisterInput
) -> User:
	"""
	Create a new user on database if not exists.

	Args:
			session (AsyncSession): Database session
			response (Response): Temporary object to set status_code
			register_data (UserRegisterInput): User type, everything needed

	Raises:
			HTTPException: raised when user already exists

	Returns:
			User: User DB model
	"""
	user_email = await UserRepository.get_user_by_email(
		session, register_data.email
	)
	user_username = await UserRepository.get_user_by_username(
		session, register_data.username
	)
	if user_email or user_username:
		response.status_code = HTTPStatus.CONFLICT
		raise HTTPException(
			status_code=HTTPStatus.CONFLICT, detail='User already exists'
		)
	register_data.password = get_password_hash(register_data.password)
	return await UserRepository.insert_user(session, register_data.to_pydantic())
