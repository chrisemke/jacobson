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

from http import HTTPStatus
from typing import Self

from faker import Faker
from httpx import AsyncClient
from jwt import decode

from database.models.user import User
from tests.integration.factories import UserFactory
from utils.settings import settings


class TestMutation:
	async def test_login_user_email_not_found(
		self: Self, client: AsyncClient, faker: Faker
	):
		mutation = """
		mutation TestLoginEmailNotFound($email: String, $password: String!) {
			login(loginData: {password: $password, email: $email}) {
				email
				id
				jwt
				username
			}
		}
		"""

		variables = {
			'email': faker.email(),
			'password': faker.password(),
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestLoginEmailNotFound',
			},
		)

		assert response.json() == {
			'data': None,
			'errors': [
				{
					'locations': [{'column': 4, 'line': 3}],
					'message': '401: Could not validate credentials',
					'path': ['login'],
				}
			],
		}
		assert response.status_code == HTTPStatus.UNAUTHORIZED

	async def test_login_user_username_not_found(
		self: Self, client: AsyncClient, faker: Faker
	):
		mutation = """
		mutation TestLoginUsernameNotFound($username: String, $password: String!) {
			login(loginData: {password: $password, username: $username}) {
				email
				id
				jwt
				username
			}
		}
		"""

		variables = {
			'username': faker.name_nonbinary(),
			'password': faker.password(),
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestLoginUsernameNotFound',
			},
		)

		assert response.json() == {
			'data': None,
			'errors': [
				{
					'locations': [{'column': 4, 'line': 3}],
					'message': '401: Could not validate credentials',
					'path': ['login'],
				}
			],
		}
		assert response.status_code == HTTPStatus.UNAUTHORIZED

	async def test_login_user_wrong_password(
		self: Self, client: AsyncClient, faker: Faker, user: User
	):
		mutation = """
		mutation TestLoginEmailNotFound($email: String, $password: String!) {
			login(loginData: {password: $password, email: $email}) {
				email
				id
				jwt
				username
			}
		}
		"""

		variables = {
			'email': user.email,
			'password': faker.password(),
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestLoginEmailNotFound',
			},
		)

		assert response.json() == {
			'data': None,
			'errors': [
				{
					'locations': [{'column': 4, 'line': 3}],
					'message': '401: Could not validate credentials',
					'path': ['login'],
				}
			],
		}
		assert response.status_code == HTTPStatus.UNAUTHORIZED

	async def test_login_email_success(
		self: Self, client: AsyncClient, user: User
	):
		mutation = """
		mutation TestLoginEmailSuccess($email: String, $password: String!) {
			login(loginData: {password: $password, email: $email}) {
				email
				id
				jwt
				username
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
				'operationName': 'TestLoginEmailSuccess',
			},
		)

		assert response.json() == {
			'data': {
				'login': {
					'email': user.email,
					'id': str(user.id),
					'jwt': response.json()['data']['login']['jwt'],
					'username': user.username,
				}
			}
		}
		assert response.status_code == HTTPStatus.OK

	async def test_login_username_success(
		self: Self, client: AsyncClient, user: User
	):
		mutation = """
		mutation TestLoginUsernameSuccess($username: String, $password: String!) {
			login(loginData: {password: $password, username: $username}) {
				email
				id
				jwt
				username
			}
		}
		"""

		variables = {
			'username': user.username,
			'password': user.clean_password,
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestLoginUsernameSuccess',
			},
		)

		assert response.json() == {
			'data': {
				'login': {
					'email': user.email,
					'id': str(user.id),
					'jwt': response.json()['data']['login']['jwt'],
					'username': user.username,
				}
			}
		}
		assert response.status_code == HTTPStatus.OK

	async def test_refresh_token_fail(self: Self, client: AsyncClient):
		mutation = """
		mutation TestRefreshTokenFail {
			refreshToken
		}
		"""
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'operationName': 'TestRefreshTokenFail',
			},
			headers={'Authorization': 'invalid_token'},
		)
		assert response.json() == {
			'data': {'refreshToken': None},
			'errors': [
				{
					'locations': [{'column': 4, 'line': 3}],
					'message': "Not Authenticated - Could not validate credentials(['DecodeError'])",
					'path': ['refreshToken'],
				}
			],
		}
		assert response.status_code == HTTPStatus.UNAUTHORIZED

	async def test_refresh_token_success(
		self: Self, client: AsyncClient, token: str
	):
		mutation = """
		mutation TestRefreshTokenSuccess {
			refreshToken
		}
		"""
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'operationName': 'TestRefreshTokenSuccess',
			},
			headers={'Authorization': token},
		)
		request_token = decode(
			token,
			settings.JWT_SECRET_KEY,
			algorithms=[settings.JWT_ALGORITHM],
		)
		response_token = decode(
			response.json()['data']['refreshToken'],
			settings.JWT_SECRET_KEY,
			algorithms=[settings.JWT_ALGORITHM],
		)
		assert response_token.get('sub') == request_token.get('sub')

	async def test_register_fail(self: Self, client: AsyncClient, faker: Faker):
		mutation = """
		mutation TestRegisterFail($password: String!, $username: String!) {
			register(registerData: {password: $password, username: $username}) {
				email
				id
				jwt
				username
			}
		}
		"""
		variables = {
			'username': faker.name_nonbinary(),
			'password': faker.password(),
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestRegisterFail',
			},
		)

		assert response.json() == {
			'data': None,
			'errors': [
				{
					'locations': [{'column': 27, 'line': 3}],
					'message': "Field 'UserRegisterInput.email' of required type "
					"'String!' was not provided.",
				}
			],
		}
		assert response.status_code == HTTPStatus.OK

	async def test_register_fail_email_duplicated(
		self: Self, client: AsyncClient, user: User, faker: Faker
	):
		mutation = """
		mutation TestRegisterFailEmailDuplicated($email: String!, $password: String!, $username: String!) {
			register(registerData: {email: $email, password: $password, username: $username}) {
				email
				id
				jwt
				username
			}
		}
		"""
		variables = {
			'email': user.email,
			'username': faker.name_nonbinary(),
			'password': faker.password(),
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestRegisterFailEmailDuplicated',
			},
		)

		assert response.json() == {
			'data': None,
			'errors': [
				{
					'locations': [{'column': 4, 'line': 3}],
					'message': '409: User already exists',
					'path': ['register'],
				}
			],
		}
		assert response.status_code == HTTPStatus.CONFLICT

	async def test_register_fail_username_duplicated(
		self: Self, client: AsyncClient, user: User, faker: Faker
	):
		mutation = """
		mutation TestRegisterFailUsernameDuplicated($email: String!, $password: String!, $username: String!) {
			register(registerData: {email: $email, password: $password, username: $username}) {
				email
				id
				jwt
				username
			}
		}
		"""
		variables = {
			'email': faker.email(),
			'username': user.username,
			'password': faker.password(),
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestRegisterFailUsernameDuplicated',
			},
		)

		assert response.json() == {
			'data': None,
			'errors': [
				{
					'locations': [{'column': 4, 'line': 3}],
					'message': '409: User already exists',
					'path': ['register'],
				}
			],
		}
		assert response.status_code == HTTPStatus.CONFLICT

	async def test_register_success(self: Self, client: AsyncClient):
		fake_user = UserFactory()
		mutation = """
		mutation TestRegisterSuccess($email: String!, $password: String!, $username: String!) {
			register(registerData: {email: $email, password: $password, username: $username}) {
				email
				id
				jwt
				username
			}
		}
		"""
		variables = {
			'email': fake_user.email,
			'username': fake_user.username,
			'password': fake_user.password,
		}
		response = await client.post(
			'/graphql',
			json={
				'query': mutation,
				'variables': variables,
				'operationName': 'TestRegisterSuccess',
			},
		)

		assert response.json() == {
			'data': {
				'register': {
					'email': fake_user.email,
					'id': response.json()['data']['register']['id'],
					'jwt': response.json()['data']['register']['jwt'],
					'username': fake_user.username,
				}
			}
		}
		assert response.status_code == HTTPStatus.OK
