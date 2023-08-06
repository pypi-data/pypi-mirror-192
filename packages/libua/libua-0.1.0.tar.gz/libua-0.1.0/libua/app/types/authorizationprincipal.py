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

import pydantic

from libua.types import ICredentialVerifier
from libua.types import IPrincipal
from .oidcprincipal import OIDCPrincipal
from .rfc9068principal import RFC9068Principal


T = TypeVar('T', bound='AuthorizationPrincipal')
S = TypeVar('S')


class AuthorizationPrincipal(pydantic.BaseModel, IPrincipal):
    __root__: RFC9068Principal | OIDCPrincipal

    @property
    def iss(self) -> str:
        return self.__root__.iss

    @property
    def client_id(self) -> str | None:
        return self.__root__.get_client_id()

    def resolve(
        self: T,
        resolve: Callable[[T],
        Awaitable[S]]
    ) -> Awaitable[S]:
        return self.__root__.resolve(resolve)

    async def verify(self, verifier: ICredentialVerifier) -> bool:
        return await self.__root__.verify(verifier)