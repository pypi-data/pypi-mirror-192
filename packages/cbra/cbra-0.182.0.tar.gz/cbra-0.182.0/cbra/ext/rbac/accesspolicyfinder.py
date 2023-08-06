# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.conf import settings
from cbra.ext import ioc

from .types import AccessPolicy
from .types import IAccessPolicyIdentifier
from .types import IAccessPolicyStorage


class AccessPolicyFinder:
    __module__: str = 'cbra.ext.rbac'
    root: AccessPolicy = AccessPolicy.parse_obj({
        'bindings': getattr(settings, 'ROOT_IAM_POLICY', [])
    })
    storage: IAccessPolicyStorage

    def __init__(
        self,
        storage: IAccessPolicyStorage = ioc.instance('AccessPolicyStorage')
    ):
        self.storage = storage

    async def find(self, resource: IAccessPolicyIdentifier) -> AccessPolicy:
        policy = await self.get(resource) or AccessPolicy()
        return self.root.merge(policy)

    async def get(self, resource: IAccessPolicyIdentifier) -> AccessPolicy | None:
        return await self.storage.get(resource)