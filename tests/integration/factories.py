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

from factory import Factory, Faker, LazyAttribute, Sequence, DictFactory
from factory.fuzzy import FuzzyChoice

from database.models.brazil import (
	Address,
	City,
	State,
	StateAcronym,
	StateAcronymName,
)
from database.models.user import User
from pydantic import ConfigDict


class StateFactory(Factory):
	class Meta:
		model = State

	acronym = FuzzyChoice(StateAcronym)
	name = LazyAttribute(lambda obj: getattr(StateAcronymName, obj.acronym).value)


class CityFactory(Factory):
	class Meta:
		model = City

	ibge = Faker('pyint')
	name = Faker('name')
	ddd = Faker('pyint', min_value=10, max_value=99)


class AddressFactory(Factory):
	class Meta:
		model = Address

	zipcode = Faker('pyint', min_value=1_000_000, max_value=99_999_999)
	state = StateFactory()
	city = CityFactory()
	neighborhood = Faker('address')
	complement = Faker('address')


class UserFactory(DictFactory):
	class Meta:
		model = User

	model_config = ConfigDict(extra='allow')

	email = LazyAttribute(lambda obj: f'{obj.username}@test.com')
	username = Sequence(lambda n: f'test{n}')
	password = LazyAttribute(lambda obj: f'{obj.username}@password123')
