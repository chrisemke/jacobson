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
from sqlmodel.ext.asyncio.session import AsyncSession

from api.address.graphql_inputs import AddressFilterInput, AddressInsertInput
from database import functions
from database.models.brazil import Address
from plugins.plugins_controller import get_zipcode_from_plugins


async def get_address(
    session: AsyncSession,
    filter: AddressFilterInput,
    page_size: PositiveInt,
    page_number: PositiveInt,
) -> list[Address]:
    """
    Get all addresses from database or all plugins.

    Parameters
    ----------
    session : AsyncSession
        get the session of database from get_session
    filter : AddressFilterInput
        Strawberry input dataclass, everything can be None
        (based on sqlmodel model)
    page_size : PositiveInt
        How many elements in each page
    page_number : PositiveInt
        Number of the page

    Returns
    -------
    list[Address]
        All addresses (db model) based on filter or empty list

    """
    result = await functions.get_address_by_dc_join_state_join_city(
        session, filter, page_size, page_number
    )
    if not result and filter.zipcode:
        result = await get_zipcode_from_plugins(session, filter.zipcode)
    return result


async def insert_address(
    session: AsyncSession, address: AddressInsertInput
) -> Address:
    """
    Insert address and city if not exists on database.

    Parameters
    ----------
    session : AsyncSession
        get the session of database from get_session
    address : AddressInsertInput
        Strict address class, all needed fields need to be passed

    Returns
    -------
    AddressType
        Address (db model)

    """
    return await functions.insert_address_by_dc(session, address)
