# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import Callable
from typing import NoReturn
from typing import TypeVar

import cbra
import fastapi

from .authorizationcontext import AuthorizationContext
from .authorizationcontext import CurrentAuthorizationContext
from .credentialverifier import CredentialVerifier
from .requestpermissions import RequestPermissions
from .nullrequestpermissions import NullRequestPermissions
from .types import RequestAborter


T = TypeVar('T', bound='Resource')


class Resource(cbra.Resource, RequestAborter):
    __abstract__: bool = True
    require_authentication: bool = False
    context: AuthorizationContext = CurrentAuthorizationContext
    permissions: RequestPermissions = NullRequestPermissions()
    verifier: CredentialVerifier = fastapi.Depends(CredentialVerifier)

    @staticmethod
    def require(name: str) -> Callable[..., Any]:
        def decorator_factory(
            func: Callable[[T], Any]
        ) -> Callable[..., Any]:
            @functools.wraps(func)
            async def f(self: T, *args: Any, **kwargs: Any) -> Any:
                await self.permissions
                if not self.has_permission(name):
                    self.deny()
                return await func(self, *args, **kwargs)
            return f
        return decorator_factory

    async def authorize(self) -> NoReturn | None:
        # Setup the authorization context and verify that the principal
        # presented a valid credential.
        await self.context.setup()
        if not await self.context.principal.verify(self.verifier):
            self.deny()

    def has_permission(self, name: str) -> bool:
        return self.permissions.has(name)