<!--
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
-->

## Unreleased

### BREAKING CHANGE

- The query has completely changed IO

### Feat

- **sqlmodel-mariadb**: add sqlmodel models, create async session, create tables on startup and add query function with beta filters
- Initial commit

### Fix

- some docker files
- continued fixing some wrong features
- **Hooks**: Validate merge branches

### Refactor

- **pydantic**: move pydantic models to sqlmodel models
- **edgedb-jacobson**: remove edgedb and legacy jacobson
- **graphql-query**: add pydantic and strawberry types to query
- start edgedb support
- create docker folders and minor fixes