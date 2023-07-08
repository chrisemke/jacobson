"""
 Jacobson is a self hosted zipcode API
 Copyright (C) 2023  Christian G. Semke

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

from os import getenv
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()


DATABASE_USER = getenv("DATABASE_USER")
DATABASE_PASSWORD = quote_plus(getenv("DATABASE_PASSWORD"))
DATABASE_HOST = getenv("DATABASE_HOST")
DATABASE_PORT = getenv("DATABASE_PORT")
DATABASE_NAME = getenv("DATABASE_NAME")

args = (
    f"mariadb+mariadbconnector://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_engine(args)

SQLModel.metadata.create_all(engine)
