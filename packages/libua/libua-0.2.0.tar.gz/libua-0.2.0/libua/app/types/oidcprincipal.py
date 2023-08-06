# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from libua.types import IPrincipal
from .jwtconsumer import JWTConsumer


class OIDCPrincipal(IPrincipal, pydantic.BaseModel, JWTConsumer):
    iss: str
    sub: int | str
    exp: int
    aud: str| list[str]
    iat: int
    auth_time: int | None = None
    nonce: str | None = None
    acr: str = "0"
    amr: list[str] = []
    azp: str | None = None
    token: str

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        authorization = values.pop('authorization')
        if not authorization:
            return values
        typ, token, jwt = cls.parse_authorization(authorization)
        if typ not in {'jwt'}:
            raise TypeError(f'Invalid JWT type: {typ[:16]}')
        values.update({**jwt.dict(), 'token': token})
        return values

    def get_client_id(self) -> str | None:
        return self.azp