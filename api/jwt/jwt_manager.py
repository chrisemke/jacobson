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

from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

import jwt
from fastapi import HTTPException
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlmodel.ext.asyncio.session import AsyncSession

from api.jwt.jwt_type import JWTClaim
from database.models.user import User
from database.repositories.user import UserRepository
from utils.settings import settings


async def get_current_user(
	session: AsyncSession,
	token: str,
) -> User:
	"""
	Get current user.

	Args:
			session (AsyncSession): Database session.
			token (str): JSON Web Token (JWT).

	Raises:
			HTTPException: When an invalid token is passed or the user does not exist

	Returns:
			User: Current user

	"""
	credentials_exception = HTTPException(
		status_code=HTTPStatus.UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={'WWW-Authenticate': 'Bearer'},
	)

	try:
		payload = jwt.decode(
			token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
		)

		if not (user_id := payload.get('sub')):
			credentials_exception.add_note('Sub not found')
			raise credentials_exception
	except (DecodeError, ExpiredSignatureError) as exc:
		credentials_exception.add_note(exc.__class__.__name__)
		raise credentials_exception from exc

	if user := await UserRepository.get_user_by_id(session, user_id):
		return user

	credentials_exception.add_note('User not found')
	raise credentials_exception


def create_access_token(data: JWTClaim) -> str:
	"""
	Create access token.

	Args:
			data (JWTClaim): Claim data.

	Returns:
			str: JSON Web Token (JWT).

	"""
	to_encode = data.copy()

	expire = datetime.now(tz=ZoneInfo(settings.TIME_ZONE)) + timedelta(
		minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
	)
	to_encode |= {'exp': expire}

	return jwt.encode(
		to_encode,  # type: ignore[arg-type]
		settings.JWT_SECRET_KEY,
		algorithm=settings.JWT_ALGORITHM,
	)
