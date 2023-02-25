from typing import Type

from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized

from app.web.app import View


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if not getattr(self.request, "admin", None):
            raise HTTPUnauthorized
        return await super(AuthRequiredMixin, self)._iter()


class AuthRequiredDecorator:
    def __new__(cls, class_: Type[View]):
        class AuthView(class_):
            async def _iter(self):
                if not getattr(self.request, "admin", None):
                    raise HTTPUnauthorized
                return await super()._iter()

        return AuthView
