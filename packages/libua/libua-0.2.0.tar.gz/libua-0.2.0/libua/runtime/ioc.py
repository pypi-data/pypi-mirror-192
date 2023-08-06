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


try:
    GOOGLE_DATASTORE_NAMESPACE: str = os.environ['GOOGLE_DATASTORE_NAMESPACE']
    GOOGLE_SERVICE_PROJECT: str = os.environ['GOOGLE_SERVICE_PROJECT']
except KeyError:
    warnings.warn(
        "Configure Google service integration using the "
        "GOOGLE_DATASTORE_NAMESPACE and GOOGLE_SERVICE_PROJECT "
        "environment variables."
    )
    sys.exit(1)
OAUTH2_SERVER: str = os.environ['OAUTH_SERVER']
OAUTH2_SERVICE_CLIENT: str = os.environ['OAUTH_SERVICE_CLIENT']


GLOBAL_DEPENDENCIES: list[dict[str, Any]] = [
    {
        'type': 'AuthorizationServerClient',
        'spec': {
            'name': 'AuthorizationServerClient',
            'qualname': 'headless.ext.oauth2.Client',
            'invoke': True,
            'kwargs': {
                'issuer': OAUTH2_SERVER,
                'client_id': OAUTH2_SERVICE_CLIENT,
                'client_secret': os.environ.get('APP_CLIENT_SECRET')\
                    or os.environ['APP_SIGNING_KEY']
            }
        }
    },
    {
        'type': 'symbol',
        'spec': {
            'name': 'DatastoreClient',
            'qualname': 'google.cloud.datastore.Client',
            'invoke': True,
            'kwargs': {
                'project': GOOGLE_SERVICE_PROJECT,
                'namespace': GOOGLE_DATASTORE_NAMESPACE
            }
        }
    },
    {
        'type': 'symbol',
        'spec': {
            'name': 'PermissionsFinder',
            'qualname': 'libua.infra.LocalPermissionsFinder'
        }
    },
    {
        'type': 'symbol',
        'spec': {
            'name': 'SubjectResolver',
            'qualname': 'libua.app.SubjectResolver'
        }
    },
]