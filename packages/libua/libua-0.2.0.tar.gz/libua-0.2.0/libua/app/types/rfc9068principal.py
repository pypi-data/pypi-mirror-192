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


class RFC9068Principal(IPrincipal, pydantic.BaseModel, JWTConsumer):
    iss: str
    aud: str| list[str]
    exp: int
    sub: str
    client_id: str
    iat: int
    jti: str
    auth_time: int | None = None
    acr: str | None = None
    amr: list[str] | None = []
    scope: str | None = None
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
        if typ not in {'application/at+jwt', 'at+jwt'}:
            raise TypeError(f'Invalid JWT type: {typ[:16]}')
        values.update({**jwt.dict(), 'token': token})
        return values

    def get_client_id(self) -> str:
        return self.client_id