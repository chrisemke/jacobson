from typing import Optional, List
from sqlmodel import Field, SQLModel, Enum, Relationship, UniqueConstraint


class Address(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("zipcode"),)
    zipcode: int
    city: int = Field(default=None, foreign_key="city.ibge")
    state: int = Field(default=None, foreign_key="state.id")
    district: str
    complement: str
    neighborhood: str
    latitude: float
    longitude: float
    altitude: float

    States: List['State'] = Relationship(back_populates='address')
    Cities: List['City'] = Relationship(back_populates='address')


class State(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    state: str

    adresses: List["Address"] = Relationship(back_populates="state")


class City(SQLModel, table=True):
    ibge: int
    name: str
    ddd: Optional[int]

    adresses: List["Address"] = Relationship(back_populates="city")
