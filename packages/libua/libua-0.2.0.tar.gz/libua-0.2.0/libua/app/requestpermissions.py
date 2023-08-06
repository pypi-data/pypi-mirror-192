# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Iterable

import fastapi
from cbra.ext import ioc
from cbra.ext.rbac import AccessPolicyFinder
from cbra.ext.rbac import BaseRequestPermissions
from cbra.ext.rbac.types import AccessPolicy

from libua.canon import AccessPolicyIdentifier
from libua.types import IPermissionsFinder
from .authorizationcontext import AuthorizationContext
from .authorizationcontext import CurrentAuthorizationContext


class RequestPermissions(BaseRequestPermissions):
    __module__: str = 'libua.app'
    context: AuthorizationContext
    granted: set[str]
    policies: AccessPolicyFinder
    policy: AccessPolicy = AccessPolicy()

    @classmethod
    def depends(cls) -> 'RequestPermissions':
        return fastapi.Depends(cls)

    def __init__(
        self,
        context: AuthorizationContext = CurrentAuthorizationContext,
        policies: AccessPolicyFinder = fastapi.Depends(AccessPolicyFinder),
        permissions: IPermissionsFinder = ioc.instance('PermissionsFinder'),
        policy_id: AccessPolicyIdentifier = AccessPolicyIdentifier.frompath()
    ):
        self.context = context
        self.granted = set()
        self.policies = policies
        self.permissions = permissions
        self.policy_id = policy_id
        self._loaded = False

    def union(self, permissions: Iterable[str]) -> set[str]:
        return self.granted & set(permissions)

    def has(self, name: str) -> bool:
        return name in self.granted

    async def setup(self) -> None:
        if not self._loaded:
            self.policy = await self.policies.find(self.policy_id)\
                or AccessPolicy()
            self.result = self.policy.match(self.context)
            self.granted = await self.permissions.find(self.result.granted())