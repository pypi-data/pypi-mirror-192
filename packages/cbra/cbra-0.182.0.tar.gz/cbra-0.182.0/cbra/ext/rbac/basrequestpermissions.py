# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generator
from typing import TypeVar


T = TypeVar('T', bound='BaseRequestPermissions')


class BaseRequestPermissions:
    __module__: str = 'cbra.ext.rbac'

    def has(self, name: str) -> bool:
        """Return a boolean indicating if the authorization context is
        granted the given permission.
        """
        raise NotImplementedError

    async def setup(self) -> None:
        raise NotImplementedError

    async def _setup(self: T) -> T:
        await self.setup()
        return self

    def __await__(self: T) -> Generator[None, None, T]:
        return self._setup().__await__()