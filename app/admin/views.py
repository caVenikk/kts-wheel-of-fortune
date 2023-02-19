from aiohttp.web import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session, get_session

from app.admin.models import Admin
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredDecorator
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        admin = await self.store.admins.get_by_email(self.data["email"])
        if not admin or not admin.is_password_valid(self.data["password"]):
            raise HTTPForbidden(reason="Incorrect email or password.")
        client_session = await new_session(self.request)
        client_session["admin"] = AdminSchema().dump(admin)
        return json_response(data=AdminSchema().dump(admin))


@AuthRequiredDecorator
class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        session = await get_session(self.request)
        admin = Admin.from_session(session)
        return json_response(data=AdminSchema().dump(admin))
