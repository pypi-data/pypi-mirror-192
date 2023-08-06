# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import ipaddress


class IAuthorizationContext:
    __module__: str = 'cbra.ext.rbac.types'
    client_id: str | None
    domain: str | None
    email: str | None
    groups: list[str]
    issuer: str | None
    remote_host: ipaddress.IPv4Address
    subject: str | None
    timestamp: datetime.datetime

    def is_client(self) -> bool:
        """Return a boolean indicating if the subject is an OAuth 2.x
        client.
        """
        raise NotImplementedError