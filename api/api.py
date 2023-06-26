from fastapi import FastAPI

from api.schema import graphql_app

api = FastAPI()
api.include_router(graphql_app, prefix="/graphql")
