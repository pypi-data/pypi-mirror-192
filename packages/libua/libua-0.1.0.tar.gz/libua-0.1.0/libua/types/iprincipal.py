# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import fastapi

from .icredentialverifier import ICredentialVerifier


T = TypeVar('T', bound='IPrincipal')
S = TypeVar('S')


class IPrincipal:
    __module__: str = 'libua.types'

    @classmethod
    def fromrequest(
        cls: type[T],
        request: fastapi.Request
    ) -> Awaitable[T] | T:
        raise NotImplementedError

    @classmethod
    def depends(cls) -> Any:
        return fastapi.Depends(cls.fromrequest)

    def resolve(
        self: T,
        resolve: Callable[[T], Awaitable[S]]
    ) -> Awaitable[S]:
        return resolve(self)

    async def verify(self, verifier: ICredentialVerifier) -> bool:
        return await verifier.verify(self)