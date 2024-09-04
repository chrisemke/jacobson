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

from typing import Self, TypedDict

from httpx import AsyncClient
from pydantic import PositiveInt

from api.address.types import DictResponse
from database.models.brazil import (
	Address,
	City,
	StateAcronym,
	StateAcronymName,
	StateCreate,
)
from plugins.protocol import Plugin
from utils.settings import settings


class CepAbertoState(TypedDict):
	sigla: str


class CepAbertoCity(TypedDict):
	ddd: int
	ibge: str
	nome: str


class CepAbertoAddress(TypedDict):
	altitude: float
	cep: str
	latitude: str
	longitude: str
	logradouro: str
	bairro: str
	complemento: str
	cidade: CepAbertoCity
	estado: CepAbertoState


class CepAberto(Plugin):
	"""
	The service of https://www.cepaberto.com/ api.

	Info:
			Currently, the request interval for each user is 1 second.
			More frequent requests will result in HTTP Error 403 Forbidden.
			The maximum request limit for each user is 10,000 per day.
	"""

	__slots__ = ('token',)

	def __init__(self: Self) -> None:
		"""
		Set token attribute.

		Args:
				self (Self): scope of current class

		Raises:
				Exception: if token does not exists.

		Todo:
				Fix generic exception

		"""
		if not settings.CEP_ABERTO_TOKEN:
			raise Exception('Token Inválido')
		self.token = settings.CEP_ABERTO_TOKEN

	async def get_address_by_zipcode(
		self: Self, zipcode: PositiveInt
	) -> DictResponse:
		"""
		Get address by zipcode.

		Args:
				self (Self): scope of the class
				zipcode (PositiveInt): Zipcode to search for,
						it should be > 1_000_000 and < 99_999_999

		Raises:
				HTTPStatusError: raise_for_status if there's any error status code

		Returns:
				DictResponse: data key have a valid address (db model);
						provider key have 'cep_aberto' str

		"""
		url = f'https://www.cepaberto.com/api/v3/cep?cep={zipcode:08}'
		headers = {'Authorization': f'Token token={self.token}'}
		async with AsyncClient() as client:
			request = await client.get(url, headers=headers)
		request.raise_for_status()

		return {
			'data': [await self._request_to_database_model(request.json())],
			'provider': 'cep_aberto',
		}

	@classmethod
	async def _request_to_database_model(
		cls, address_data: CepAbertoAddress
	) -> Address:
		"""
		Receive a json/dict and return an Address object.

		Args:
				address_data (CepAbertoAddress): here's a dict example:
						{
							"altitude": 760.0,
							"cep": "01001000",
							"latitude": "-23.5479099981",
							"longitude": "-46.636",
							"logradouro": "Praça da Sé",
							"bairro": "Sé",
							"complemento": "- lado ímpar",
							"cidade": {
								"ddd": 11,
								"ibge": "3550308",
								"nome": "São Paulo"
							},
							"estado": {
								"sigla": "SP"
							}
						}

		Returns:
				Address: Database model

		"""
		acronym = address_data['estado']['sigla']
		state = StateCreate(
			acronym=StateAcronym(acronym),
			name=getattr(StateAcronymName, acronym).value,
		)

		city = City(
			ibge=int(address_data['cidade']['ibge']),
			name=address_data['cidade']['nome'],
			ddd=address_data['cidade']['ddd'],
		)

		logradouro = (
			f'{address_data['logradouro']} {address_data.get('complemento', '')}'
		).strip()

		return Address(
			zipcode=int(address_data['cep']),
			state=state,
			city=city,
			neighborhood=address_data['bairro'],
			complement=logradouro,
			coordinates={
				'latitude': float(address_data['latitude']),
				'longitude': float(address_data['longitude']),
				'altitude': address_data.get('altitude'),
			}
			if address_data.get('latitude') and address_data.get('longitude')
			else None,
		)
