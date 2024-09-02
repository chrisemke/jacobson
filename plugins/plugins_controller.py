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

from asyncio import as_completed, create_task

from pydantic import PositiveInt

from api.address.types import DictResponse
from plugins.cep_aberto.cep_aberto import CepAberto
from plugins.viacep.viacep import ViaCep


async def get_zipcode_from_plugins(
	zipcode: PositiveInt,
) -> DictResponse:
	"""
	Async call to all plugins at decame time
	The first task that returns successfully returns and cancels the others.

	Args:
			zipcode (PositiveInt): zipcode needed to search address on api's

	Returns:
			DictResponse: 'data' key has all addresses
					(db model) based on filter or empty list;
					'provider' key has the service provider plugin

	Todo:
			Create all tasks based on config
			Add logs

	"""
	tasks = []
	for service in [CepAberto, ViaCep]:
		try:
			service_instance = service()
			tasks.append(create_task(service_instance.get_address_by_zipcode(zipcode)))
		except Exception:
			# async insert logs
			...

	for task in as_completed(tasks):
		try:
			result = await task
			break
		except Exception as e:
			print('Erro:', e)
			result = {'data': [], 'provider': 'Plugins'}
			# there is no address found in this task
			# async insert logs

	return result
