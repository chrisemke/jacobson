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

from typing import Any, Self

from fastapi import HTTPException
from strawberry import BasePermission, Info
from strawberry.permission import PermissionExtension

from jacobson.api.context import Context


class IsAuthenticated(BasePermission):
	message = 'Not Authenticated'

	async def has_permission(
		self: Self, source: Any, info: Info[Context], **kwargs: Any
	) -> bool:
		"""
		strawberry default function to see if user has permission.

		Args:
				self (Self): Scope of current class
				source (Any): Strawberry default field
				info (Info[Context]): Custom context class
				kwargs (Any): Strawberry default field

		Returns:
				bool: True if authentication is successful

		"""
		request = info.context.request

		if 'Authorization' not in request.headers:
			return False

		try:
			if await info.context.user():
				return True
		except HTTPException as e:
			self.message = f'Not Authenticated - {e.detail}({e.__notes__})'
			response = info.context.response

			response.status_code = e.status_code

			if e.headers:
				for k, v in e.headers.items():
					response.headers[k] = v

		return False


AuthExtension = PermissionExtension([IsAuthenticated()])
