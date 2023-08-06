"""Declares :class:`IClient`."""
import datetime
from typing import cast
from typing import Any
from typing import Union

import ckms
import ckms.jose
import pydantic
from ckms.jose import PayloadCodec
from ckms.core.models import JSONWebSignature
from ckms.types import IKeychain
from ckms.types import JSONWebToken
from ckms.types import JSONWebKey
from ckms.types import JSONWebKeySet

from .granttype import GrantType
from .isubject import ISubject
from .redirecturl import RedirectURL
from .responsetype import ResponseType


class IClient(pydantic.BaseModel):
    """Specifies the interface of OAuth 2.0 client objects.

    An OAuth 2.0 client can be determined from various parameters in an
    HTTP request.

    For requests to the :term:`Authorization Endpoint`, the client is
    specified by the ``client_id`` parameter. This is the case for both
    public clients and confidential clients.

    The client is determined for :term:`Token Endpoint` requests by
    either the ``client_id`` parameter in the request body if the
    client is public, or by the credentials provided in the
    ``Authorization`` header. In the latter case, the ``client_id``
    parameter is absent in the request body.
    """
    __module__: str = 'cbra.ext.oauth2.types'
    __abstract__: bool = True

    client_id: str

    @classmethod
    async def fromquery(
        cls,
        clients: type,
        required: bool = False
    ) -> Any:
        """Return a callable that resolves the current client from the
        query parameters.
        """
        raise NotImplementedError

    @classmethod
    def fromdict(cls, params: dict[str, Any]) -> 'IClient':
        """Construct a new client from a dictionary."""
        raise NotImplementedError

    @classmethod
    def configure(cls, **kwargs: Any) -> 'IClient':
        """Configures the class with the given parameters."""
        return cast(IClient, type(cls.__name__, (cls,), kwargs))

    async def get_codec(self, codec: PayloadCodec) -> PayloadCodec:
        """Return a new :class:`ckms.jose.PayloadCodec` configured to use
        the client keys for encryption.
        """
        raise NotImplementedError

    async def get_jwks(self) -> JSONWebKeySet:
        """Return a :class:`ckms.types.JSONWebKeySet` instance holding the
        signing and encryption keys of the client.
        """
        raise NotImplementedError

    def as_subject(self) -> ISubject:
        """Return a :class:`~cbra.ext.oauth2.types.ISubject` implementation
        representing the client itself. For use with the client credentials
        grant.
        """
        raise NotImplementedError

    def allows_audience(self, issuer: str, audience: set[str]) -> bool:
        """Return a boolean indicating if the client allows the issueing
        of access token for the given audiences set `audience`.
        """
        raise NotImplementedError

    def allows_scope(self, scope: set[str]) -> bool:
        """Return a boolean indicating if the client allows the given scope."""
        raise NotImplementedError

    def allows_grant_type(self, grant_type: GrantType) -> bool:
        """Return a boolean indicating if the client allows the given grant type."""
        raise NotImplementedError

    def allows_origin(self, origin: str | None) -> bool:
        """Return a boolean indicating if the client allows the given origin in the
        context of Cross-Origin Resource Sharing (CORS).
        """
        raise NotImplementedError

    def allows_response_mode(self, response_mode: Any) -> bool:
        """Return a boolean indicating if the client allows the given response
        mode.
        """
        raise NotImplementedError

    def allows_response_type(self, response_type: ResponseType) -> bool:
        """Return a boolean indicating if the client allows the given response
        type.
        """
        raise NotImplementedError

    def can_issue_multiple(self) -> bool:
        """Return a boolean indicating if the client allows issueing
        access tokens to multiple audiences.
        """
        raise NotImplementedError

    def get_default_redirect(self) -> str:
        """Return the default redirect URL, if specified."""
        raise NotImplementedError

    def get_consent_url(self, scope: set[str]) -> str:
        """Return the URL at which the resource owner can grant consent
        for the given scope to this client.
        """
        raise NotImplementedError

    def get_encryption_keys(self) -> list[JSONWebKey]:
        """Return the list of encryption keys used by the client."""
        raise NotImplementedError

    def get_id_token_claims(self, now: int) -> dict[str, Any]:
        """Return a dictionary holding the claims that this client
        adds to an ID token.
        """
        raise NotImplementedError

    def get_redirect_url(
        self,
        url: Union[str, RedirectURL] | None = None,
        fatal: bool = True
    ) -> RedirectURL | None:
        raise NotImplementedError

    def get_refresh_token_expires(self, now: int) -> int:
        """Return a :class:`datetime.datetime` instance indicating the
        Time-To-Live (TTL) of a refresh token.
        """
        raise NotImplementedError

    def get_sector_identifier(self) -> Any:
        """Return the sector identifier used by this client."""
        raise NotImplementedError

    def get_subject_id(self, subject: ISubject) -> int:
        """Return the subject identifier to add to an access token or ID
        token.
        """
        raise NotImplementedError

    def is_confidential(self) -> bool:
        """Return a boolean indicating if the client is confidential and
        must authenticate itself.
        """
        raise NotImplementedError

    def is_first_party(self) -> bool:
        """Return a boolean indicating if this is a first-party client
        that does not have to obtain consent.
        """
        raise NotImplementedError

    def is_public(self) -> bool:
        """Return a boolean indicating if the client is public."""
        raise NotImplementedError

    def assigns_ppid(self) -> bool:
        """Return a boolean indicating if this client assigns a PPID."""
        raise NotImplementedError

    async def create_refresh_token(
        self,
        codec: ckms.jose.PayloadCodec,
        subject: ISubject,
        authorization_id: int,
        token_id: int,
        expires: datetime.datetime | None = None
    ) -> str:
        """Create a new refresh token using the client parameters."""
        raise NotImplementedError

    async def issue_token(
        self,
        *,
        codec: ckms.jose.PayloadCodec,
        issuer: str,
        audience: list[str] | str | set[str] | None,
        subject: ISubject,
        using: str,
        ttl: int,
        scope: set[str]
    ) -> str:
        """Issue an access token encoded as a JSON Web Token (JWT)
        as defined in :rfc:`9068`. Return a string containing the
        token.
        """
        raise NotImplementedError

    async def verify_jws(
        self,
        jws: JSONWebSignature
    ) -> bool:
        """Verify a :class:`~JSONWebSignature` using the public
        keys associated to the client.
        """
        raise NotImplementedError

    async def verify_jwt(
        self,
        token: Union[bytes, str],
        decrypter: IKeychain | None,
        compact_only: bool = False,
        audience: str | None = None
    ) -> JSONWebToken:
        """Verifies a JSON Web Token (JWT) using the public key of the
        client.

        Args:
            token (byte-sequence or string): the JWT to deserialize and
                verify.
            decrypter: a :class:`~IKeychain` implementation that has the
                private keys to decrypt, if the payload is a JWE.
            compact_only (bool): indicates if only compact deserialization
                is allowed. If `compact_only` is ``True`` and the token
                is not compact serialized, an exception is raised.

        Returns
            A :class:`dict` containing the claims in the JWT.
        """
        raise NotImplementedError