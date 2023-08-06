# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import logging

from cbra.ext import ioc
from headless.ext.oauth2 import Client

from libua.types import ISubjectResolver
from libua.types import IPrincipal
from .types import NullPrincipal
from .types import RFC9068Principal
from .types import NullSubject
from .types import RequestAborter
from .types import Subject


class SubjectResolver(ISubjectResolver, RequestAborter):
    __module__: str = 'libua.app'
    client: Client
    logger: logging.Logger = logging.getLogger('uvicorn')

    def __init__(
        self,
        client: Client = ioc.inject('AuthorizationServerClient')
    ):
        self.client = client

    @functools.singledispatchmethod # type: ignore
    async def resolve(self, principal: IPrincipal) -> Subject:
        raise TypeError(f'{type(principal).__name__}')

    @resolve.register
    async def resolve_null(
        self,
        principal: NullPrincipal
    ) -> Subject:
        return NullSubject()

    @resolve.register
    async def resolve_rfc9068(
        self,
        principal: RFC9068Principal
    ) -> Subject:
        await self.client.discover()
        if principal.iss != self.client.metadata.issuer:
            self.logger.critical('Client used token from untrusted issuer.')
            return NullSubject()
        return Subject(
            sub=principal.sub
        )