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

from datetime import datetime
from enum import StrEnum
from typing import TypedDict
from uuid import uuid4

from pydantic import UUID4, PositiveInt
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import (
	Field,
	Relationship,
	SQLModel,
)
from strawberry import enum


@enum
class StateAcronym(StrEnum):
	AC = 'AC'
	AL = 'AL'
	AP = 'AP'
	AM = 'AM'
	BA = 'BA'
	CE = 'CE'
	DF = 'DF'
	ES = 'ES'
	GO = 'GO'
	MA = 'MA'
	MT = 'MT'
	MS = 'MS'
	MG = 'MG'
	PA = 'PA'
	PB = 'PB'
	PR = 'PR'
	PE = 'PE'
	PI = 'PI'
	RJ = 'RJ'
	RN = 'RN'
	RS = 'RS'
	RO = 'RO'
	RR = 'RR'
	SC = 'SC'
	SP = 'SP'
	SE = 'SE'
	TO = 'TO'


class StateAcronymName(StrEnum):
	AC = 'Acre'
	AL = 'Alagoas'
	AP = 'Amapá'
	AM = 'Amazonas'
	BA = 'Bahia'
	CE = 'Ceará'
	DF = 'Distrito Federal'
	ES = 'Espírito Santo'
	GO = 'Goiás'
	MA = 'Maranhão'
	MT = 'Mato Grosso'
	MS = 'Mato Grosso do Sul'
	MG = 'Minas Gerais'
	PA = 'Pará'
	PB = 'Paraíba'
	PR = 'Paraná'
	PE = 'Pernambuco'
	PI = 'Piauí'
	RJ = 'Rio de Janeiro'
	RN = 'Rio Grande do Norte'
	RS = 'Rio Grande do Sul'
	RO = 'Rondônia'
	RR = 'Roraima'
	SC = 'Santa Catarina'
	SP = 'São Paulo'
	SE = 'Sergipe'
	TO = 'Tocantins'


class StateBase(SQLModel):
	acronym: StateAcronym = Field(
		unique=True,
		index=True,
	)
	name: str | None


class StateCreate(StateBase):
	name: str


class State(StateCreate, table=True):
	__tablename__ = 'states'

	id: UUID4 | None = Field(default_factory=uuid4, primary_key=True)


class CityBase(SQLModel):
	ibge: PositiveInt = Field(
		unique=True,
		index=True,
	)
	name: str | None
	ddd: int | None = None


class CityCreate(CityBase):
	name: str


class City(CityCreate, table=True):
	__tablename__ = 'cities'

	id: UUID4 | None = Field(default_factory=uuid4, primary_key=True)


class Coordinates(TypedDict):
	latitude: float
	longitude: float
	altitude: float | None


class AddressBase(SQLModel):
	zipcode: int | None = Field(None, gt=1_000_000, lt=99_999_999)
	neighborhood: str | None = None
	complement: str | None = None
	coordinates: Coordinates | None = None


class Address(AddressBase, table=True):
	__tablename__ = 'addresses'

	id: UUID4 = Field(default_factory=uuid4, primary_key=True)

	zipcode: int = Field(unique=True, index=True, gt=1_000_000, lt=99_999_999)

	state_id: UUID4 = Field(foreign_key='states.id')
	state: State = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})

	city_id: UUID4 = Field(foreign_key='cities.id')
	city: City = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})

	neighborhood: str
	complement: str | None = None
	coordinates: Coordinates | None = Field(None, nullable=True, sa_type=JSONB)

	updated_at: datetime | None = Field(
		default_factory=datetime.now,
		nullable=False,
		sa_column_kwargs={
			'onupdate': datetime.now,
		},
	)
