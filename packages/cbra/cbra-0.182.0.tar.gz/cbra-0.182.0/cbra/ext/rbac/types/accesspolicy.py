# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
from typing import TypeVar

import pydantic

from .authorizationresult import AuthorizationResult
from .iauthorizationcontext import IAuthorizationContext
from .iprincipal import IPrincipal
from .predefinedrolebinding import PredefinedRoleBinding


T = TypeVar('T', bound='AccessPolicy')


class AccessPolicy(pydantic.BaseModel):
    bindings: list[PredefinedRoleBinding] = []

    @pydantic.validator('bindings')
    def postprocess_bindings(
        cls,
        value: list[PredefinedRoleBinding]
    ) -> list[PredefinedRoleBinding]:
        bindings: dict[str, PredefinedRoleBinding] = {}
        conditional: list[PredefinedRoleBinding] = []
        for binding in value:
            if binding.has_conditions():
                conditional.append(binding)
                continue
            if binding.role not in bindings:
                bindings[binding.role] = binding
                continue
            bindings[binding.role] = bindings[binding.role].merge(binding)
        return list(bindings.values()) + conditional

    def has(self, role: str) -> bool:
        return role in [x.role for x in self.bindings]

    def match(self, ctx: IAuthorizationContext) -> AuthorizationResult:
        roles: dict[str, set[IPrincipal]] = collections.defaultdict(set)
        for binding in self.bindings:
            roles[binding.role].update(binding.match(ctx))
        return AuthorizationResult(
            roles=roles
        )

    def merge(self: T, policy: T) -> T:
        bindings: dict[str, PredefinedRoleBinding] = collections.OrderedDict()
        for binding in self.bindings:
            bindings[binding.role] = binding
        for binding in policy.bindings:
            if binding.role in bindings:
                bindings[binding.role] = bindings[binding.role].merge(binding)
            else:
                bindings[binding.role] = binding
        return self.parse_obj({'bindings': list(bindings.values())})

    def __or__(self: T, policy: T) -> T:
        return self.merge(policy)