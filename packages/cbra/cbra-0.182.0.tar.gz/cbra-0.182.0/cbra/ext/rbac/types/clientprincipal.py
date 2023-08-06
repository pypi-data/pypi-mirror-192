# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Callable
from typing import Generator
from typing import TypeVar

from canonical import EmailAddress
from pydantic.validators import str_validator

from .baseprincipal import BasePrincipal
from .iauthorizationcontext import IAuthorizationContext


T = TypeVar('T', bound='ClientPrincipal')


class ClientPrincipal(BasePrincipal):
    kind: str = 'client'

    @classmethod
    def __get_validators__(
        cls: type[T]
    ) -> Generator[Callable[..., T | str], None, None]:
        yield str_validator
        yield lambda cls, value: str.lower(value)
        yield cls.parse_value
        yield EmailAddress.validate
        yield cls.validate

    @classmethod
    def validate(cls: type[T], v: str) -> T:
        client_id, issuer = str.split(str(v), '@')
        return cls(issuer, client_id)

    def __init__(self, issuer: str, client_id: str):
        self.issuer = issuer
        self.client_id = client_id

    def get_value(self) -> str:
        return f'{self.kind}:{self.client_id}@{self.issuer}'

    def match(self, ctx: IAuthorizationContext) -> bool:
        return all([
            ctx.is_client(),
            ctx.client_id==self.client_id,
            ctx.issuer==self.issuer
        ])

    def __repr__(self) -> str:
        return f"ClientPrincipal(issuer='{self.issuer}', client_id='{self.client_id}')"