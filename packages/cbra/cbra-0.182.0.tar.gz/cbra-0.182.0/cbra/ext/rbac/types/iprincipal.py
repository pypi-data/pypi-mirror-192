# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .iauthorizationcontext import IAuthorizationContext


class IPrincipal:
    __module__: str = 'cbra.ext.rbac.types'

    def match(self, ctx: IAuthorizationContext) -> bool:
        raise NotImplementedError

    def __lt__(self, y: Any) -> bool:
        raise NotImplementedError