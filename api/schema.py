from strawberry import Schema, field, type
from strawberry.fastapi import GraphQLRouter

# from jacobson.database.functions.functions import get_address, create_address


@type
class Address:
    zipcode: int
    city: int
    state: int
    district: str
    complement: str
    neighborhood: str
    latitude: float
    longitude: float
    altitude: float


@type
class Query:
    all_address: list[Address] = field(resolver=get_address)


# @type
# class Mutation:
#     create_address: Address = Address field(resolver=create_address)


# schema =   # , mutation=Mutation)

graphql_app = GraphQLRouter(Schema(query=Query))
