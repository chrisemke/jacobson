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

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


class Address(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("zipcode"),)
    zipcode: int
    city: int = Field(default=None, foreign_key="city.ibge")
    state: int = Field(default=None, foreign_key="state.id")
    district: str
    complement: str
    neighborhood: str
    latitude: float
    longitude: float
    altitude: float

    States: list["State"] = Relationship(back_populates="address")
    Cities: list["City"] = Relationship(back_populates="address")


class State(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    state: str

    adresses: list["Address"] = Relationship(back_populates="state")


class City(SQLModel, table=True):
    ibge: int
    name: str
    ddd: int | None

    adresses: list["Address"] = Relationship(back_populates="city")
