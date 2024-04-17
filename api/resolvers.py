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

from pydantic import PositiveInt

from api.address.inputs import AddressFilterInput, AddressInsertInput
from database import functions
from database.models.brazil import Address


async def get_address(
    filter: AddressFilterInput,
    page_size: PositiveInt,
    page_number: PositiveInt,
) -> list[Address | None]:
    result = await functions.get_address_by_dc_join_state_join_city(
        filter, page_size, page_number
    )
    if not result:
        try:
            ...
            # result = async get from plugins
        except Exception:
            ...
            # there is no address found
        else:
            ...
            # async insert on database
    return result


async def insert_address(address: AddressInsertInput) -> Address:
    return await functions.insert_address_by_dc(address)
