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

from database.functions import insert_address
from database.models.brazil import Address
from plugins.cep_aberto.cep_aberto import CepAberto
from plugins.viacep.viacep import ViaCep


async def get_zipcode_from_plugins(
    zipcode: PositiveInt,
) -> list[Address]:
    """
    Async call to all plugins at decame time
    The first task that returns successfully returns and cancels the others.

    Parameters
    ----------
    zipcode : PositiveInt
        zipcode needed to search address on api's

    Returns
    -------
    list[Address]
        List that contains only one Address (db model)
        it's a list for compatibility with database query

    Todo:
    ----
    - Create all tasks based on config
    - Add logs

    """
    tasks = []
    for service in [CepAberto, ViaCep]:
        try:
            service_instance = service()
            tasks.append(
                create_task(service_instance.get_address_by_zipcode(zipcode))
            )
        except Exception:
            # async insert logs
            ...

    result = []
    for task in as_completed(tasks):
        try:
            result = await task
            break
        except Exception as e:
            print('Erro:', e)
            # there is no address found in this task
            # async insert logs

    if result:
        insert_task = create_task(insert_address(result[0]))
        # insert log
        print(insert_task)

    return result
