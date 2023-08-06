# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from libua.canon import Role


VIEWER_PERMISSIONS: list[str] =[
    'resourcemanager.projects.get',
    'resourcemanager.projects.list',
    'resourcemanager.projects.getiam',
    'resourcemanager.organizations.get',
    'resourcemanager.organizations.list',
    'resourcemanager.organizations.getiam',
    'esg.services.get',
    'esg.services.list',
    'iam.roles.get',
    'iam.roles.list',
]

EDITOR_PERMISSIONS: list[str] = [
    'resourcemanager.projects.create',
    'resourcemanager.projects.update',
    'resourcemanager.projects.delete',
    'resourcemanager.projects.setiam',
    'resourcemanager.organizations.setiam',
    'esg.services.create',
    'esg.services.onboard',
    'esg.services.update',
    'esg.services.delete',
    'esg.services.suspend',
    'esg.services.synchronize',
    'iam.roles.create',
    'iam.roles.update',
    'iam.roles.delete',
    'iam.roles.disable',
    *VIEWER_PERMISSIONS
]

OWNER_PERMISSIONS: list[str] = [
    'iam.roles.create',
    'iam.roles.update',
    'iam.roles.delete',
    *EDITOR_PERMISSIONS,
    *VIEWER_PERMISSIONS
]


ROLES: dict[str, Role] = {
    'roles/editor': Role(
        name='editor',
        title='Editor',
        includedPermissions=EDITOR_PERMISSIONS
    ),
    'roles/owner': Role(
        name='owner',
        title='Owner',
        includedPermissions=OWNER_PERMISSIONS
    ),
    'roles/viewer': Role(
        name='viewer',
        title='Viewer',
        includedPermissions=VIEWER_PERMISSIONS
    ),
}

class LocalPermissionsFinder:

    async def find(self, roles: set[str]) -> set[str]:
        permissions: set[str] = set()
        for role in roles:
            binding = ROLES.get(role)
            if binding is None:
                continue
            permissions.update(binding.permissions)
        return permissions