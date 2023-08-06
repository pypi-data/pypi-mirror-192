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
from typing import Any

from cbra.ext import ioc
from headless.ext.oauth2 import Client

from libua.types import ICredentialVerifier
from .types import NullPrincipal
from .types import RFC9068Principal


class CredentialVerifier(ICredentialVerifier):
    __module__: str = 'libua.app'
    client: Client
    logger: logging.Logger = logging.getLogger('uvicorn')

    def __init__(
        self,
        client: Client = ioc.inject('AuthorizationServerClient')
    ):
        self.client = client

    @functools.singledispatchmethod # type: ignore
    async def verify(self, principal: Any) -> bool:
        self.logger.critical(
            'Verification of %s is not implemented, refusing.',
            type(principal).__name__
        )
        return False

    @verify.register
    async def verify_null(
        self,
        principal: NullPrincipal
    ) -> bool:
        return True

    @verify.register
    async def verify_rfc9068(
        self,
        principal: RFC9068Principal
    ) -> bool:
        return await self.client.verify(principal.token)