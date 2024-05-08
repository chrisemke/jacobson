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

from typing import Self

from pytest import mark

from api.address.inputs import AddressFilterInput, AddressInsertInput
from api.address.types import AddressType
from api.schema import Mutation, Query
from database.models.brazil import Address, City, State, StateAcronym


class TestQuery:
    @mark.asyncio
    async def test_all_address(self: Self, mocker):
        state = State(acronym=StateAcronym.SP, name='São Paulo', id=None)
        city = City(ibge=3550308, name='São Paulo', ddd=11, id=None)
        address = Address(
            zipcode=1001000,
            neighborhood='Sé',
            complement='Praça da Sé - lado ímpar',
            id=None,
            state=state,
            city=city,
        )
        mocker.patch('api.schema.get_address', return_value=[address])
        out = await Query().all_address(AddressFilterInput())
        for i in out:
            assert isinstance(i, AddressType)

            assert i.to_pydantic().model_dump() == address.model_dump()


class TestMutation:
    @mark.asyncio
    async def test_create_address(self: Self, mocker):
        state = State(acronym=StateAcronym.SP, name='São Paulo', id=None)
        city = City(ibge=3550308, name='São Paulo', ddd=11, id=None)
        address = AddressInsertInput(
            zipcode=1001000,
            neighborhood='Sé',
            complement='Praça da Sé - lado ímpar',
            state=state,
            city=city,
        )

        mocker.patch(
            'api.schema.insert_address', return_value=address.to_pydantic()
        )
        out = await Mutation().create_address(address)

        assert isinstance(out, AddressType)

        assert (
            out.to_pydantic().model_dump()
            == address.to_pydantic().model_dump()
        )
