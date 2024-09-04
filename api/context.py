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

from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.fastapi import BaseContext

from api.jwt.jwt_manager import get_current_user
from database.engine import T_AsyncSession
from database.models.user import User


class Context(BaseContext):
	request: Request | WebSocket
	background_tasks: BackgroundTasks
	response: Response
	_current_user: User | None

	def __init__(self: Self, session: T_AsyncSession):
		"""Generate context database session."""
		self.session = session
		self._current_user = None

	async def user(self: Self) -> User | None:
		"""
		Get database user based on jwt.

		Args:
				self (Self): Scope of current class

		Returns:
				User | None: User (db model) if exists

		"""
		if self._current_user:
			return self._current_user

		if authorization := self.request.headers.get('Authorization', None):
			self._current_user = await get_current_user(self.session, authorization)
			return self._current_user

		return None
