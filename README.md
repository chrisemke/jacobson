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

# jacobson
self-hosted zipcode API


### The initial structure I imagined would be:
```
*api query/get* -> search in database -> if there is any result return;
else async call to all plugins that are configured, return and insert on database
```
```
*api mutation/post* -> manually update or insert zipcodes
```
```
call to tell the api to update some register from plugins that are configured
```

# ROADMAP:

## DONE (v0.1)
- [x] git hooks (pre-commit)
- [x] ORM (SqlModel)
- [x] Api's support services (cepaberto, viacep...)
- [x] Unit tests (pytest)
- [x] Migrations and data seed (Alembic)

## DONE (v0.2)
- [x] Fix database session with get_db or get_session
- [x] Start Integration tests
- [x] Docs (mkdocs + mkdocs-material[to beautify] + mkdocstrings[to transform docstrings into docs])
- [x] mkdocs on gh pages and/or readthedocs
- [x] Taskipy
- [x] Re-enable Coordinates on database and api's (only cep_aberto available)

## TODO (Needed for v0.3)
- [ ] Add log support (loguru? or OpenTelemetry?)
- [ ] Custom exceptions
- [ ] Auth (pyjwt+pwdlib)
- [ ] More test (unit and integration)

## TODO (Needed until v1.0)
- [ ] Populate the database with zip codes and cities
- [ ] Automate migrations tests?
- [ ] separate tests into groups to be run selectively
- [ ] git hooks to run fast and slow tests
- [ ] Resolve all code issues (TODO's on docstrings)
- [ ] CI and CI tests
- [ ] freeze versions on docker and pyproject
- [ ] Better structure for services (plugin-like)
- [ ] Send 'total' information on api requests for pagination

### TODO (nice to have)
- [ ] add option to seed all cities (or chosen list)
- [ ] add option to seed all zip codes (or chosen list)
- [ ] add graphql schema generator on git hooks
- [ ] move from docker-compose to a podman pod
- [ ] study mypyc viability
- [ ] jacobson logo

# DEV
The idea is to just run this command and podman will run the entire dev environment

obs: before this command you need to create the .env (see sample.env for example)

to run podman as expected, you will need the packages "podman", "podman-compose" and "aardvark-dns"

```bash
podman compose up -d --build
```

You can access the api at localhost port 8000 /graphql
```
http://127.0.0.1:8000/graphql
```
