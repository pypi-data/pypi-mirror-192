"""Declares :class:`ISubject`."""
from typing import Any
from typing import Coroutine

from ckms.core.models import JSONWebSignature
from ckms.types import JSONWebKey


class ISubject:
    """Specifies the interface to which all subject implementations
    must provide.
    """
    __module__: str = 'cbra.ext.oauth2.types'

    #: The subject identifier. The type and semantics are implementation specific,
    #: but the concrete implementation must ensure that :attr:`sub` is JSON
    #: serializable.
    sub: int | str

    #: Identifies the client in which the context subject was
    #: instantiated, or ``None``.
    client_id: int | str | None = None

    #: Used for testing purposes only.
    #client_scope: defaultdict[str, set[str]]

    def allows_scope(self, scope: Any) -> bool:
        """Return a boolean indicating that the requested scope `scope`
        was allowed by the subject.
        """
        raise NotImplementedError

    def get_claim(self, name: str) -> Any:
        """Return the specified OIDC claim for this subject."""
        raise NotImplementedError

    def get_identifier(self, public: bool = False) -> Any:
        """Return the identifier for this Subject."""
        raise NotImplementedError

    def register_public_key(self, key: JSONWebKey) -> None:
        """Register a public key for the :class:`ISubject`."""
        raise NotImplementedError

    def verify(
        self,
        jws: JSONWebSignature
    ) -> bool | Coroutine[Any, Any, bool]:
        """Verifies a JSON Web Signature (JWS) using the keys that were
        previously registered by the :term:`Subject`.
        """
        raise NotImplementedError