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

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.address.graphql_inputs import AddressFilterInput, AddressInsertInput
from database.engine import engine
from database.models.brazil import Address, City, State


async def page_to_offset(
    page_size: PositiveInt, page_number: PositiveInt
) -> PositiveInt:
    """
    Calculate the database offset based on page size and number.

    Parameters
    ----------
    page_size : PositiveInt
        How many elements in each page
    page_number : PositiveInt
        Number of the page

    Returns
    -------
    PositiveInt
        The database offset

    """
    if page_number <= 1:
        return 0
    return page_size * (page_number - 1)


async def get_address_by_dc_join_state_join_city(
    filter: AddressFilterInput,
    page_size: PositiveInt = 10,
    page_number: PositiveInt = 1,
) -> list[Address]:
    """
    Query addresses by the strawberry dataclass.

    Parameters
    ----------
    filter : AddressFilterInput
        Strawberry input dataclass, everything can be None
        (based on sqlmodel model)
    page_size : PositiveInt, optional
        How many elements in each page, by default 10
    page_number : PositiveInt, optional
        Number of the page, by default 1

    Returns
    -------
    list[Address]
        All addresses (db model) based on filter or empty list

    Todo:
    ----
    - Fix Joins with async client

    """
    query = (
        select(Address)
        .options(
            joinedload('*'),
        )
        .limit(page_size)
        .offset(await page_to_offset(page_size, page_number))
    )

    if filter.zipcode:
        query = query.where(Address.zipcode == filter.zipcode)
    else:
        if filter.neighborhood:
            query = query.where(Address.neighborhood == filter.neighborhood)
        if filter.complement:
            query = query.where(Address.complement == filter.complement)
        if filter.city:
            query = query.where(City.ibge == filter.city.ibge)
        if filter.state:
            query = query.where(State.acronym == filter.state.acronym.value)

    async with AsyncSession(engine) as session:
        adresses_result = await session.exec(query)
        addresses = adresses_result.unique().all()

    return list(addresses)


async def insert_address_by_dc(address: AddressInsertInput) -> Address:
    """
    Create address by the strawberry dataclass.

    Parameters
    ----------
    address : AddressInsertInput
        Strawberry input dataclass, strict (based on sqlmodel model)

    Returns
    -------
    Address
        Single model instance, should be converted for strawberry

    Raises
    ------
    HTTPException
        If city.ibge is not found on database: 404 error

    """
    address_model = address.to_pydantic()

    async with AsyncSession(engine) as session:
        state_query = select(State).where(
            State.acronym == address.state.acronym.value
        )
        state_result = await session.exec(state_query)
        state = state_result.one()
        address_model.state = state

        city_query = select(City).where(City.ibge == address.city.ibge)
        city_result = await session.exec(city_query)
        city = city_result.one_or_none()
        if not city:
            raise HTTPException(status_code=404, detail='City not found')
        address_model.city = city

        session.add(address_model)
        await session.commit()
        await session.refresh(address_model)

        query = (
            select(Address)
            .options(
                joinedload('*'),
            )
            .where(Address.id == address_model.id)
        )
        adress_result = await session.exec(query)
        address_model = adress_result.unique().one()

    return address_model


async def insert_address(address: Address) -> None:
    """
    Insert addresses and city if not exists in background.

    Parameters
    ----------
    address : Address
        Address instance based on database models

    """
    async with AsyncSession(engine) as session:
        state_query = select(State).where(
            State.acronym == address.state.acronym.value
        )
        state_result = await session.exec(state_query)
        state = state_result.one()
        address.state = state

        city_query = select(City).where(City.ibge == address.city.ibge)
        city_result = await session.exec(city_query)
        city = city_result.one_or_none()
        if city:
            address.city = city

        session.add(address)
        await session.commit()
