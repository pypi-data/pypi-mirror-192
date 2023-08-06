# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar
from typing import Union

import fastapi
from cbra.ext.rbac.types import IAccessPolicyIdentifier

from .organizationidentifier import OrganizationIdentifier
from .organizationprojectidentfier import OrganizationProjectIdentifier


T = TypeVar('T', bound='AccessPolicyIdentifier')


class AccessPolicyIdentifier(IAccessPolicyIdentifier):
    __root__: Union[
        OrganizationProjectIdentifier,
        OrganizationIdentifier
    ]

    @classmethod
    def frompath(cls: type[T]) -> T:
        def f(request: fastapi.Request) -> Any:
            return cls.parse_obj(request.path_params).__root__
        return fastapi.Depends(f)