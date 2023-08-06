# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .requestpermissions import RequestPermissions


class NullRequestPermissions(RequestPermissions):
    __module__: str = 'libua.app'

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    async def setup(self) -> None:
        pass

    def has(self, name: str) -> bool:
        return False