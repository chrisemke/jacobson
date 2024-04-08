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

# TODO
- [x] git hooks (pre-commit)
- [x] SqlModel
- [ ] Api's support plugin-like (cepaberto, brazilapi...)
- [ ] Tests (pytest)
- [ ] Docs (mkdocs)
- [ ] fix podman pod for all devs (see jacobson-dev.yaml)
- [ ] Alembic migrations


# DEV
The idea is to just run this command and podman will run the entire dev environment
```bash
podman compose up -d --build
```
