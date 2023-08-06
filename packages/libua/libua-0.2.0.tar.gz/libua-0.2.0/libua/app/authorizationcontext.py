# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import TypeVar

import fastapi
from cbra.ext import ioc
from cbra.ext.rbac import BaseAuthorizationContext

from libua.types import ISubject
from libua.types import ISubjectResolver
from .types import Principal
from .types import NullSubject


T = TypeVar('T', bound='AuthorizationContext')


class AuthorizationContext(BaseAuthorizationContext):
    _awaited: bool = False
    principal: Principal
    resolver: ISubjectResolver
    _request: fastapi.Request
    _subject: ISubject = NullSubject()

    @classmethod
    def depends(cls) -> 'AuthorizationContext':
        async def f(self: T = fastapi.Depends(cls)) -> T:
            await self.setup()
            return self
        return fastapi.Depends(f)

    def __init__(
        self,
        request: fastapi.Request,
        resolver: ISubjectResolver = ioc.instance('SubjectResolver'),
        principal: Principal = Principal.depends()
    ):
        self.principal = principal
        self.resolver = resolver
        self._request = request

    def is_authenticated(self) -> bool:
        return not isinstance(self.principal, NullSubject)

    async def setup(self):
        if not self._awaited:
            self._subject = await self.principal.resolve(self.resolver.resolve)
            self._awaited = True
            
            # TODO: We need to check if it is secure to remove the protocol in the
            # issuer if we are later using the issuer to determine permissions.
            super().__init__(
                issuer=re.sub(r'^https\:\/\/', '', self.principal.iss) if self.principal.iss else None,
                subject=self._subject.sub,
                email=None,
                client_id=self.principal.client_id,
                remote_host=str(self._request.client.host)\
                    if self._request.client\
                    else None
            )


CurrentAuthorizationContext: AuthorizationContext = AuthorizationContext.depends()