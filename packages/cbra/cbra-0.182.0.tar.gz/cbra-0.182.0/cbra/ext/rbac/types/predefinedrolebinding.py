# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

import pydantic

from .clientprincipal import ClientPrincipal
from .iauthorizationcontext import IAuthorizationContext
from .iprincipal import IPrincipal
from .userprincipal import UserPrincipal


T = TypeVar('T', bound='PredefinedRoleBinding')


class PredefinedRoleBinding(pydantic.BaseModel):
    role: str
    members: list[ClientPrincipal | UserPrincipal]

    @pydantic.validator('members', allow_reuse=True)
    def postprocess_members(
        cls,
        members: list[IPrincipal]
    ) -> list[IPrincipal]:
        return list(sorted(set(members)))

    def has_conditions(self) -> bool:
        return False

    def match(self, ctx: IAuthorizationContext) -> list[IPrincipal]:
        """Return a boolean indicating if the context matches
        the bound roles.
        """
        matched: list[IPrincipal] = []
        for principal in self.members:
            if not principal.match(ctx):
                continue
            matched.append(principal)
        return matched

    def merge(self: T, binding: T) -> T:
        if self.role != binding.role:
            raise ValueError('Can not merge different roles.')
        members: set[IPrincipal] = set()
        members.update(binding.members)
        members.update(self.members)
        return self.parse_obj({
            'role': self.role,
            'members': [str(x) for x in members]
        })