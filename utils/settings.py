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
from pydantic_settings import BaseSettings, SettingsConfigDict


class UrlValidate(BaseModel):
    url: MySQLDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', frozen=True
    )

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: PositiveInt
    DATABASE_NAME: str

    CEP_ABERTO_TOKEN: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URL(self) -> str:
        url = (
            'mysql+asyncmy://'
            f'{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@'
            f'{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        )

        return str(UrlValidate(url=url).url)


settings = Settings()
