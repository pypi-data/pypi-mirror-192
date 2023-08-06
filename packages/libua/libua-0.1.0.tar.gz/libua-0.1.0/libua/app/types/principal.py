# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import fastapi
import pydantic

from libua.types import IPrincipal
from libua.types import ICredentialVerifier
from .authorizationprincipal import AuthorizationPrincipal
from .nullprincipal import NullPrincipal


T = TypeVar('T', bound='Principal')
S = TypeVar('S')


class Principal(IPrincipal):
    impl: AuthorizationPrincipal | NullPrincipal

    @property
    def iss(self) -> str | None:
        return self.impl.iss

    @property
    def client_id(self) -> str | None:
        return self.impl.client_id

    @classmethod
    def fromrequest(
        cls: type[T],
        request: fastapi.Request
    ) -> T:
        principal = NullPrincipal()
        if request.headers.get('Authorization'):
            try:
                principal = AuthorizationPrincipal.parse_obj({
                    'authorization': request.headers['Authorization']
                })
            except pydantic.ValidationError:
                raise
                principal = NullPrincipal()
        return cls(principal)

    def __init__(self, impl: AuthorizationPrincipal | NullPrincipal):
        self.impl = impl

    def resolve(
        self: T,
        resolve: Callable[[T],
        Awaitable[S]]
    ) -> Awaitable[S]:
        return self.impl.resolve(resolve)

    async def verify(self, verifier: ICredentialVerifier) -> bool:
        return await self.impl.verify(verifier)

    def __repr__(self) -> str:
        return repr(self.impl)