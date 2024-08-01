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

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.schema import graphql_app
from utils.settings import settings

app = FastAPI()
app.include_router(graphql_app, prefix='/graphql')

if settings.DEV:
	app.mount(
		'/',
		StaticFiles(directory='documentation/site', html=True),
		name='mkdocs',
	)
	templates = Jinja2Templates(directory='documentation/site')

	@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
	async def mkdocs(request: Request) -> HTMLResponse:
		"""
		Response de mkdocs site, from result of build.
		ONLY ENABLED IN DEV MODE.

		Args:
				request (Request): Fastapi Request

		Returns:
				HTMLResponse: Mkdocs static site from documentation/site

		"""
		return templates.TemplateResponse(name='index.html', request=request)
