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

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from utils.settings import settings

engine = create_async_engine(
	settings.DATABASE_URL,
	echo=settings.DEV,
	future=True,
	pool_size=20,
	max_overflow=20,
	pool_recycle=3600,
)


async def get_session() -> (
	AsyncGenerator[AsyncSession, None]
):  # pragma: no cover
	"""Create and yield database async session."""
	async with AsyncSession(engine, expire_on_commit=False) as session:
		yield session


T_AsyncSession = Annotated[AsyncSession, Depends(get_session)]
