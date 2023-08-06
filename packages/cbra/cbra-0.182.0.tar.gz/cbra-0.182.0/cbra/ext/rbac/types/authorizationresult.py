# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .iprincipal import IPrincipal


class AuthorizationResult:
    __module__: str = 'cbra.ext.rbac.types'
    roles: dict[str, set[IPrincipal]]

    def __init__(
        self,
        roles: dict[str, set[IPrincipal]]
    ) -> None:
        self.roles = roles

    def granted(self) -> set[str]:
        """Return the set of roles that are granted to the principal."""
        return {x for x in self.roles if self.roles.get(x)}

    def has(self, role: str) -> bool:
        """Return a boolean indicating if the context allowed the
        given role.
        """
        return bool(self.roles.get(role))

    def __repr__(self) -> str:
        return f'AuthorizationResult({",".join([x for x in self.roles])})'