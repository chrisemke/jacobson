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

from pydantic import UUID4
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database.models.user import User


class UserRepository:
	@staticmethod
	async def get_user_by_id(session: AsyncSession, id: UUID4) -> User | None:
		"""
		Get user by id if exists.

		Args:
				session (AsyncSession): Database session
				id (UUID4): user primary key uuid

		Returns:
				User | None: User DB model or None

		"""
		query = await session.exec(select(User).where(User.id == id))
		return query.one_or_none()

	@staticmethod
	async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
		"""
		Get user by email if exists.

		Args:
				session (AsyncSession): Database session
				email (str): user email unique key

		Returns:
				User | None: User DB model or None

		"""
		query = await session.exec(select(User).where(User.email == email))
		return query.one_or_none()

	@staticmethod
	async def get_user_by_username(
		session: AsyncSession, username: str
	) -> User | None:
		"""
		Get user by username if exists.

		Args:
				session (AsyncSession): Database session
				username (str): user username unique key

		Returns:
				User | None: User DB model or None

		"""
		query = await session.exec(select(User).where(User.username == username))
		return query.one_or_none()

	@staticmethod
	async def insert_user(session: AsyncSession, user: User) -> User:
		"""
		Insert user based on model.

		Args:
				session (AsyncSession): Database session
				user (User): User DB model

		Returns:
				User: User DB model
		"""
		session.add(user)
		await session.commit()

		return user
