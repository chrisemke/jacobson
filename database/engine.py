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

from urllib.parse import quote_plus

from pydantic import (
    BaseModel,
    MySQLDsn,
    PositiveInt,
    computed_field,
)
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel


class UrlValidate(BaseModel):
    url: MySQLDsn


class Database(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: PositiveInt
    DATABASE_NAME: str

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URL(self) -> str:
        url = (
            'mysql+asyncmy://'
            f'{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@'
            f'{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        )

        return str(UrlValidate(url=url).url)

    class Config:
        """A config class to make model immutable."""

        env_file = '.env'
        frozen = True


database = Database()

engine = create_async_engine(
    database.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
)

async def init_db() -> None:
    async with engine.begin() as session:
        await session.run_sync(SQLModel.metadata.create_all)
