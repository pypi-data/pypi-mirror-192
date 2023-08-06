# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.rbac.types import AccessPolicy
from cbra.ext.rbac.types import IAccessPolicyStorage
from cbra.ext.rbac.types import IAccessPolicyIdentifier


class LocalAccessPolicyStorage(IAccessPolicyStorage):
    __module__: str = 'libua.infra'

    async def get(self, policy_id: IAccessPolicyIdentifier) -> AccessPolicy | None:
        return None