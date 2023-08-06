# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .rolelaunchstage import RoleLaunchStage


class Role(pydantic.BaseModel):
    name: str = pydantic.Field(
        default=...,
        title='Name',
        description=(
            'The name of the role.\n\n'
            'When `Role` is used in a creation request, the '
            'role name must not be set.\n\n'
        ),
        min_length=3,
        max_length=63
    )

    title: str = pydantic.Field(
        default=...,
        description='Optional. A human-readable title for the role.',
        min_length=2,
        max_length=63,
    )

    description: str | None =  pydantic.Field(
        default=None,
        title='Description',
        description='A human-readable description for this `Role`.'
    )

    permissions: list[str] = pydantic.Field(
        default=[],
        title='Permissions',
        alias='includedPermissions',
        description=(
            'The names of the permissions this role '
            'grants when bound in an IAM policy.'
        )
    )

    stage: RoleLaunchStage = pydantic.Field(
        default=RoleLaunchStage.alpha,
        title='Stage',
        description='The current launch stage of the role.'
    )

    @pydantic.validator('permissions')
    def postprocess_permissions(
        cls,
        permissions: list[str]
    ) -> list[str]:
        return list(sorted(set(permissions)))

    class Config:
        allow_population_by_field_name: bool = True