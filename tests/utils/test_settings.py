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

from utils.settings import Settings


class TestSettings:
    def test_all_settings(self: Self, monkeypatch):
        expected = {
            'DATABASE_USER': 'teste',
            'DATABASE_PASSWORD': 'teste',
            'DATABASE_HOST': 'jacobson_db_1',
            'DATABASE_PORT': '3306',
            'DATABASE_NAME': 'test',
            'CEP_ABERTO_TOKEN': 'token',
            'DATABASE_URL': 'mysql+asyncmy://teste:teste@jacobson_db_1:3306/test',
        }
        for k, v in expected.items():
            monkeypatch.setenv(k, v)

        expected['DATABASE_PORT'] = int(expected['DATABASE_PORT'])
        assert Settings().model_dump() == expected
