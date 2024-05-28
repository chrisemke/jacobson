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
from strawberry import Schema, field, type
from strawberry.fastapi import GraphQLRouter

from api.address.graphql_inputs import AddressFilterInput, AddressInsertInput
from api.address.graphql_types import AddressType
from api.resolvers import get_address, insert_address


@type
class Query:
    @field
    async def all_address(
        self,
        filter: AddressFilterInput,
        page_size: PositiveInt = 10,
        page_number: PositiveInt = 1,
    ) -> list[AddressType]:
        """
        Query all addresses from database or all plugins.

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
        list[AddressType]
            All addresses (db model converted to strawberry dataclass)
            based on filter or empty list

        """
        return list(
            map(
                AddressType.from_pydantic,
                await get_address(filter, page_size, page_number),
            )
        )


@type
class Mutation:
    @field
    async def create_address(self, address: AddressInsertInput) -> AddressType:
        """
        Insert address and city if not exists on database.

        Parameters
        ----------
        address : AddressInsertInput
            Strict address class, all needed fields need to be passed

        Returns
        -------
        AddressType
            Address (db model converted to strawberry dataclass)

        """
        return AddressType.from_pydantic(await insert_address(address))


schema = Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter[object, object](schema)
