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

from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.address.inputs import AddressInput
from database.engine import engine
from database.models.brazil import Address, City, State


async def get_address_by_dc_join_state_join_city(
    filter: AddressInput,
) -> list[Address | None]:
    query = (
        select(Address)
        .join(State)
        .join(City)
        .options(
            joinedload(Address.state),
            joinedload(Address.city),
        )
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
        result = (await session.exec(query)).unique().all()

    return result


async def create_address():
    ...
