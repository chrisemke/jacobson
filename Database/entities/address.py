from typing import Opitional
from sqlmodel import Field, SQLModel, Enum, Relationship

# class Address(SQLModel, table=True):
#     __table_args__ = (UniqueConstraint('cep'))
#     zipcode: int = Field(default=None)
#     neighborhood: str
#     street: str
#     city: str
#     state: strStatusChoices = Field(sa_column=Column(Enum(StatusChoices)))
#     service: str
#     type: str
#     latitude: str
#     longitude: str


class Address(SQLModel, table=True):
    __table_args__ = UniqueConstraint("zipcode")
    zipcode: int = Field(default=None)
    city: int = Field(default=None, foreign_key="city.ibge")
    state: int = Field(default=None, foreign_key="state.id")
    district: str
    complement: str
    neighborhood: str
    latitude: float
    longitude: float
    altitude: float


class State(SQLModel, table=True):
    id: Opitional[int] = Field(default=None, primary_key=True)
    state: str

    adresses: List["Address"] = Relationship(back_populates="state")


class City(SQLModel, table=True):
    ibge: int
    name: str
    ddd: Opitional[int]

    adresses: List["Address"] = Relationship(back_populates="city")
