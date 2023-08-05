# Copyright (C) 2022 Cochise Ruhulessin <cochiseruhulessin@gmail.com>
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
"""Declares :class:`IPrincipal`."""
from typing import Any

from ckms.types import ClaimSet
from ckms.types import JSONWebToken


class IPrincipal:
    """Specifies the interface for all principal implementations."""
    __module__: str = 'cbra.types'

    #: The subject identifier; establishes the identity of the current user,
    #: application or service account that issued a request to the HTTP
    #: server.
    sub: int | str | None

    @classmethod
    def fromclaimset(
        cls,
        claims: Any
    ) -> 'IPrincipal':
        """Instantiate a new :class:`IPrincipal` using the claims provided with a
        JSON Web Token (JWT).
        """
        raise NotImplementedError

    def get_auth_time(self) -> int:
        """Return an integer indicating the date/time at which the
        principal last authenticated, in seconds since the UNIX epoch.
        """
        raise NotImplementedError

    def get_current_scope(self) -> set[str]:
        """Return the scope that is currrently granted to the principal."""
        raise NotImplementedError

    def get_session_claims(self) -> dict[str, Any]:
        """Return a dictionary holding claims about the current
        session that is established by the principal.
        """
        raise NotImplementedError

    def has_scope(
        self,
        scope: str | set[str]
    ) -> bool:
        """Return a boolean indicating if the :class:`IPrincipal` is
        authorized to use the given `scope`.
        """
        raise NotImplementedError

    def is_authenticated(self) -> bool:
        """Return a boolean indicating if the principal is authenticated. Most
        commonly this will imply that :attr:`sub` is not ``None``.
        """
        raise NotImplementedError

    def __bool__(self) -> bool:
        return self.is_authenticated()