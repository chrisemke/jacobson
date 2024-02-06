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

from sqlmodel import Session, select

from jacobson.database.engine import engine
from jacobson.database.entities.address import Address

# def create_livros(titulo: str, pessoa_id: int):
#     livro = Livro(titulo=titulo, pessoa_id=pessoa_id)

#     with Session(engine) as session:
#         session.add(livro)
#         session.commit()
#         session.refresh(livro)

#     return livro

# def get_livros():
#     query = select(Livro).options(joinedload('*'))
#     with Session(engine) as session:
#         result = session.execute(query).scalars().unique().all()

#     return result


def create_address(zipcode: int):
    address = Address(zipcode)

    with Session(engine) as session:
        session.add(address)
        session.commit()
        session.refresh(address)

    return address


def get_address(
    zipcode: int | None = None,
    city: str | None = None,
    state: str | None = None,
    limit: int = 5,
):
    query = select(Address)

    if zipcode:
        query = query.where(Address.zipcode == zipcode)
    if city:
        query = query.where(Address.city == city)
    if state:
        query = query.where(Address.state == state)
    if limit:
        query = query.limit(limit)

    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    return result
