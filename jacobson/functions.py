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
