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

from typing import Self
from urllib.parse import quote_plus

from pydantic import (
	BaseModel,
	PositiveInt,
	PostgresDsn,
	computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class UrlValidate(BaseModel):
	url: PostgresDsn


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file='.env', env_file_encoding='utf-8', frozen=True
	)
	DEV: bool

	DATABASE_USER: str
	DATABASE_PASSWORD: str
	DATABASE_HOST: str
	DATABASE_PORT: PositiveInt = 5432
	DATABASE_NAME: str

	JWT_SECRET_KEY: str
	JWT_ALGORITHM: str = 'HS256'
	ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 30

	TIME_ZONE: str = 'UTC'

	CEP_ABERTO_TOKEN: str | None = None

	@computed_field  # type: ignore[prop-decorator]
	@property
	def DATABASE_URL(self: Self) -> str:
		"""Generate and validate database url based on other fields."""
		url = (
			'postgresql+psycopg://'
			f'{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@'
			f'{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
		)

		return str(UrlValidate(url=url).url)


settings = Settings()
