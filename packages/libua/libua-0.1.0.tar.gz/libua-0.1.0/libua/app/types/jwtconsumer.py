# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ckms.types import JSONWebToken
from ckms.jose import Decoder
from fastapi.security.utils import get_authorization_scheme_param


class JWTConsumer:

    @staticmethod
    def parse_authorization(authorization: str) -> tuple[str, str, JSONWebToken]:
        scheme, token = get_authorization_scheme_param(authorization)
        if str.lower(scheme or '') != 'bearer':
            raise ValueError('not an RFC 9068 access token.')
        typ = None
        try:
            jose, jwt = Decoder.introspect(token)
            for header in jose.headers:
                if header.typ is None:
                    continue
                typ = str.lower(header.typ)
                break
            else:
                typ = None
        except Exception:
            jwt = None
        if jwt is None:
            raise ValueError('could not decode the Authorization header as a JWT.')
        if typ is None:
            raise TypeError(
                'untyped JWT can not be used as an access token.'
            )
        return typ, token, jwt