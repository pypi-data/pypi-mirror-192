# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import sys
import warnings
from typing import Any

from ckms.core import parse_dsn


__all__: list[str] = [
    'OAUTH2_SERVER',
    'OAUTH2_SERVICE_CLIENT',
    'APP_ENCRYPTION_KEY',
    'APP_SIGNING_KEY',
    'PII_ENCRYPTION_KEY',
    'PII_INDEX_KEY',
    'ROOT_IAM_POLICY',
    'KEYCHAIN'
]

APP_ENCRYPTION_KEY: str = 'enc'

APP_SIGNING_KEY: str = 'sig'

PII_ENCRYPTION_KEY: str = 'pii'

PII_INDEX_KEY: str = 'idx'

KEYCHAIN: dict[str, Any] = {
    APP_ENCRYPTION_KEY: {
        **parse_dsn(os.environ['APP_ENCRYPTION_KEY']),
        'tags': ['oauth2-client']
    },
    APP_SIGNING_KEY: {
        **parse_dsn(os.environ['APP_SIGNING_KEY']),
        'tags': ['oauth2-client']
    },
    PII_ENCRYPTION_KEY: parse_dsn(os.environ['PII_ENCRYPTION_KEY']),
    PII_INDEX_KEY: parse_dsn(os.environ['PII_INDEX_KEY']),
}

#: Default authorization server and client
try:
    OAUTH2_SERVER: str = os.environ['OAUTH_SERVER']
    OAUTH2_SERVICE_CLIENT: str = os.environ['OAUTH_SERVICE_CLIENT']
except KeyError:
    warnings.warn(
        "Authorization server must be configured through "
        "environment using the OAUTH_SERVER and "
        "OAUTH_SERVICE_CLIENT variables.")
    sys.exit(1)


ROOT_IAM_POLICY: list[dict[str, str | list[str]]] = []