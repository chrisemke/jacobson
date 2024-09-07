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
from uuid import uuid4

import pytest
from faker.generator import Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from testcontainers.postgres import PostgresContainer

from api.app import app
from api.security import get_password_hash
from database.engine import get_session
from database.models.brazil import State
from database.models.user import User
from tests.integration.factories import (
	AddressFactory,
	CityFactory,
	UserFactory,
)


@pytest.fixture(scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
	"""Database engine."""
	with PostgresContainer(
		'docker.io/library/postgres:16-alpine', driver='psycopg'
	) as postgres:
		yield create_async_engine(postgres.get_connection_url(), echo=True)


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
	"""Database session."""
	async with engine.begin() as trans:
		await trans.run_sync(SQLModel.metadata.create_all)

	async with AsyncSession(engine, expire_on_commit=False) as session:
		yield session

		await session.rollback()

	async with engine.begin() as trans:
		await trans.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(autouse=True)
async def state_data_seed(session):
	"""Insert all states on first run."""
	result = await session.exec(select(State).limit(1))
	if not result.one_or_none():
		states = [
			{'id': uuid4(), 'acronym': 'AC', 'name': 'Acre'},
			{'id': uuid4(), 'acronym': 'AL', 'name': 'Alagoas'},
			{'id': uuid4(), 'acronym': 'AP', 'name': 'Amapá'},
			{'id': uuid4(), 'acronym': 'AM', 'name': 'Amazonas'},
			{'id': uuid4(), 'acronym': 'BA', 'name': 'Bahia'},
			{'id': uuid4(), 'acronym': 'CE', 'name': 'Ceará'},
			{'id': uuid4(), 'acronym': 'DF', 'name': 'Distrito Federal'},
			{'id': uuid4(), 'acronym': 'ES', 'name': 'Espírito Santo'},
			{'id': uuid4(), 'acronym': 'GO', 'name': 'Goiás'},
			{'id': uuid4(), 'acronym': 'MA', 'name': 'Maranhão'},
			{'id': uuid4(), 'acronym': 'MT', 'name': 'Mato Grosso'},
			{'id': uuid4(), 'acronym': 'MS', 'name': 'Mato Grosso do Sul'},
			{'id': uuid4(), 'acronym': 'MG', 'name': 'Minas Gerais'},
			{'id': uuid4(), 'acronym': 'PA', 'name': 'Pará'},
			{'id': uuid4(), 'acronym': 'PB', 'name': 'Paraíba'},
			{'id': uuid4(), 'acronym': 'PR', 'name': 'Paraná'},
			{'id': uuid4(), 'acronym': 'PE', 'name': 'Pernambuco'},
			{'id': uuid4(), 'acronym': 'PI', 'name': 'Piauí'},
			{'id': uuid4(), 'acronym': 'RJ', 'name': 'Rio de Janeiro'},
			{'id': uuid4(), 'acronym': 'RN', 'name': 'Rio Grande do Norte'},
			{'id': uuid4(), 'acronym': 'RS', 'name': 'Rio Grande do Sul'},
			{'id': uuid4(), 'acronym': 'RO', 'name': 'Rondônia'},
			{'id': uuid4(), 'acronym': 'RR', 'name': 'Roraima'},
			{'id': uuid4(), 'acronym': 'SC', 'name': 'Santa Catarina'},
			{'id': uuid4(), 'acronym': 'SP', 'name': 'São Paulo'},
			{'id': uuid4(), 'acronym': 'SE', 'name': 'Sergipe'},
			{'id': uuid4(), 'acronym': 'TO', 'name': 'Tocantins'},
		]
		await session.run_sync(lambda ses: ses.bulk_insert_mappings(State, states))


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
	"""Test client."""
	app.dependency_overrides[get_session] = lambda: session

	async with AsyncClient(
		app=app, base_url='http://dummy', http2=True
	) as test_client:
		yield test_client

	app.dependency_overrides.clear()


@pytest.fixture
async def address(session: AsyncSession):
	"""Test address."""
	address = AddressFactory()

	state_query = select(State).where(
		State.acronym == address.state.acronym.value
	)
	state_result = await session.exec(state_query)
	state = state_result.one()

	address.state = state

	session.add(address)
	await session.commit()

	return address


@pytest.fixture
async def city(session: AsyncSession):
	"""Test city."""
	city = CityFactory()

	session.add(city)
	await session.commit()

	return city


@pytest.fixture
async def user(faker: Generator, session: AsyncSession) -> User:
	"""Test user."""
	password = faker.password()
	user = UserFactory(password=get_password_hash(password))

	session.add(user)
	await session.commit()
	await session.refresh(user)

	user.__dict__['clean_password'] = password

	return user


@pytest.fixture
async def token(client: AsyncClient, user: User) -> str:
	"""JWT valid token."""
	mutation = """
		mutation LoginToJWT($email: String, $password: String!) {
			login(loginData: {password: $password, email: $email}) {
				jwt
			}
		}
	"""

	variables = {
		'email': user.email,
		'password': user.clean_password,
	}
	response = await client.post(
		'/graphql',
		json={
			'query': mutation,
			'variables': variables,
			'operationName': 'LoginToJWT',
		},
	)
	return response.json()['data']['login']['jwt']
