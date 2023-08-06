# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ipaddress
from typing import TypeVar

import fastapi

from .types import IAuthorizationContext


T = TypeVar('T', bound='BaseAuthorizationContext')


class BaseAuthorizationContext(IAuthorizationContext):
    __module__: str = 'cbra.ext.rbac'

    @classmethod
    def fromrequest(cls: type[T]) -> T:
        raise NotImplementedError

    @classmethod
    def inject(cls: type[T]) -> T:
        return fastapi.Depends(cls.fromrequest)

    def __init__(
        self,
        issuer: str | None,
        subject: str | None = None,
        email: str | None = None,
        client_id: str | None = None,
        remote_host: str | ipaddress.IPv4Address | None = None
    ):
        self.client_id = client_id
        self.email = email
        self.issuer = issuer
        self.subject = subject
        if remote_host is None:
            remote_host = '127.0.0.1'
        if isinstance(remote_host, str):
            remote_host = ipaddress.IPv4Address(remote_host)
        self.remote_host = remote_host

    def is_client(self) -> bool:
        return all([
            self.client_id == self.subject,
            self.client_id is not None,
            self.subject is not None,
        ])