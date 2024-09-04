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

from database.models.user import User


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
					'locations': [{'column': 5, 'line': 3}],
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
					'locations': [{'column': 5, 'line': 3}],
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
					'locations': [{'column': 5, 'line': 3}],
					'message': '401: Could not validate credentials',
					'path': ['login'],
				}
			],
		}
		assert response.status_code == HTTPStatus.UNAUTHORIZED
