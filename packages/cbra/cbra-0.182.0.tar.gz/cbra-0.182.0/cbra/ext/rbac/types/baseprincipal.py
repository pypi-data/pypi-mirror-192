# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

from .iauthorizationcontext import IAuthorizationContext
from .iprincipal import IPrincipal


T = TypeVar('T', bound='BasePrincipal')


class BasePrincipal(IPrincipal):
    kind: str

    @classmethod
    def parse_value(cls, v: str) -> str:
        if not str.startswith(v, f'{cls.kind}:'):
            raise ValueError(f"value is not a {cls.__name__}")
        return str.split(v, ':', 1)[1]

    def get_value(self) -> str:
        raise NotImplementedError

    def match(self, ctx: IAuthorizationContext) -> bool:
        raise NotImplementedError

    def __eq__(self: T, y: T) -> bool: # type: ignore[override]
        if not isinstance(y, type(self)): return NotImplemented
        return str(self) == str(y)

    def __hash__(self) -> int:
        return hash(str(self))

    def __lt__(self: T, y: T) -> bool: # type: ignore[override]
        if not isinstance(y, type(self)):
            return type(self).__name__ < type(y).__name__
        return str(self) < str(y)

    def __str__(self) -> str:
        return f'{self.kind}:{self.get_value()}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}({str(self)})'