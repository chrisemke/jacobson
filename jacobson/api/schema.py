from typing import Optional, List
from strawberry import type, field, Schema
from strawberry.fastapi import GraphQLRouter
# from jacobson.database.functions.db_function import 


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
    all_address: List[Address] = field(resolver=get_address)


@type
class Mutation:
    create_address: Address = field(resolver=create_address)


schema = Schema(
    query=Query,
    mutation=Mutation
)

graphql_app = GraphQLRouter(schema)