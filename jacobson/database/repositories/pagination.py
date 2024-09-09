"""
Jacobson is a self hosted zipcode API
Copyright (C) 2023-2024 Christian G. Semke.

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


def page_to_offset(
	page_size: PositiveInt, page_number: PositiveInt
) -> PositiveInt:
	"""
	Calculate the database offset based on page size and number.

	Args:
			page_size (PositiveInt): How many elements in each page
			page_number (PositiveInt): Number of the page

	Returns:
			PositiveInt: The database offset

	"""
	if page_number <= 1:
		return 0
	return page_size * (page_number - 1)
