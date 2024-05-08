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

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from utils.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
)


async def init_db() -> None:
    async with engine.begin() as session:
        await session.run_sync(SQLModel.metadata.create_all)
