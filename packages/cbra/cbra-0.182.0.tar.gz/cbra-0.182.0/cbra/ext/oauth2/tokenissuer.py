"""Declares :class:`TokenIssuer`."""
import functools
import inspect
import logging
import typing
from typing import Any

from ckms.core import Keychain
from ckms.jose import PayloadCodec
from ckms.types import JSONWebToken
from ckms.types import Malformed

from cbra.conf import settings
from cbra.params import ServerKeychain
from .authorization import Authorization
from .exceptions import InvalidClient
from .exceptions import InvalidGrant
from .exceptions import InvalidScope
from .exceptions import ForbiddenScope
from .exceptions import AssertionReplayed
from .params import CurrentServerMetadata
from .params import LocalIssuer
from .params import OIDCTokenBuilder
from .params import ServerCodec
from .params import SubjectRepository
from .params import TransientStorage
from .types import AuthorizationCodeGrant
from .types import AuthorizationIdentifier
from .types import BaseGrant
from .types import ClientCredentialsGrant
from .types import GrantType
from .types import IClient
from .types import IOIDCTokenBuilder
from .types import IStorage
from .types import ISubject
from .types import ISubjectRepository
from .types import ITokenIssuer
from .types import JWTBearerAssertionGrant
from .types import NullRefreshToken
from .types import RefreshToken
from .types import RefreshTokenGrant
from .types import RefreshTokenIdentifier
from .types import ScopedGrant
from .types import SessionGrant
from .types import ServerMetadata
from .types import TokenException
from .types import TokenResponse
from .utils import classproperty # type: ignore


SIGNING_KEY: str = getattr(settings, 'OAUTH_SIGNING_KEY', 'sig')


class TokenIssuer(ITokenIssuer):
    """Issues a token for various grant types."""
    __module__: str = 'cbra.ext.oauth2'
    logger: logging.Logger = logging.getLogger('uvicorn')

    #: The default :class:`~ckms.core.Keychain` instance used by the
    #: server.
    keychain: Keychain

    #: The transient storage used.
    storage: IStorage

    #: OpenID Connect token builder
    openid: IOIDCTokenBuilder

    @classproperty
    def grant_types_supported(cls) -> typing.List[str]:
        return [
            GrantType.authorization_code.value,
            GrantType.refresh_token.value,
            GrantType.client_credentials.value,
            GrantType.jwt_bearer.value
        ]

    def __init__(
        self,
        subjects: ISubjectRepository = SubjectRepository,
        keychain: Keychain = ServerKeychain,
        codec: PayloadCodec = ServerCodec,
        metadata: ServerMetadata = CurrentServerMetadata,
        issuer: str = LocalIssuer,
        storage: IStorage = TransientStorage,
        openid: IOIDCTokenBuilder = OIDCTokenBuilder
    ):
        self.codec = codec
        self.issuer = issuer
        self.keychain = keychain
        self.metadata = metadata
        self.openid = openid
        self.storage = storage
        self.subjects = subjects

    def is_local_issued(self, claims: JSONWebToken) -> bool:
        """Return a boolean indicating if the claimset was issued
        by the local server.
        """
        return self.issuer == claims.iss

    @functools.singledispatchmethod
    async def grant(
        self,
        dto: BaseGrant
    ) -> TokenResponse:
        """Dispatches a request to the **Token Endpoint** to the
        appropriate handler for its ``grant_type``.
        """
        self.logger.critical("Invalid grant requested: %s", dto.grant_type.value)
        raise TokenException(
            code='invalid_grant',
            description=(
                "The server allows but has not implemented the use of the "
                f"'{dto.grant_type.value}' grant."
            )
        )

    @grant.register
    async def grant_refresh_token(
        self,
        grant: RefreshTokenGrant
    ) -> TokenResponse:
        """Rotate the existing refresh token and issue a new access token
        and refresh token.
        """
        client = grant.get_client()
        if not client.allows_audience(self.issuer, grant.resource):
            raise TokenException(
                code='invalid_grant',
                description=(
                    "The Client does not allow the creation of access tokens "
                    "for the given resource."
                )
            )
        key = RefreshTokenIdentifier.parse_jwt(client.client_id, grant.refresh_token)
        token = await self.storage.get(key)
        if token is None or not await token.verify(grant.refresh_token):
            if token is not None:
                self.logger.info(
                    "Signature validation failure for token (id: %s)",
                    token.id
                )
            raise TokenException(
                code='invalid_grant',
                description="The refresh token is invalid, expired or revoked."
            )
        assert isinstance(token, RefreshToken) # nosec
        if not token.allows_scope(grant.scope):
            raise TokenException(
                code='invalid_grant',
                description=(
                    "The requested scope exceeds the scope that was "
                    "granted by the Resource Owner."
                )
            )

        subject = await self.subjects.get(
            client=client,
            subject_id=token.sub,
            force_public=True
        )
        if subject is None:
            raise TokenException(
                code='invalid_grant',
                description="The refresh token is invalid, expired or revoked."
            )

        result = TokenResponse(
            access_token=await client.issue_token(
                codec=self.codec,
                using=SIGNING_KEY,
                issuer=self.metadata.issuer,
                audience=grant.get_audience(),
                subject=subject,
                ttl=self.default_ttl,
                scope=set(grant.scope or []) or set(token.scope)
            ),
            id_token=None,
            state=None,
            token_type="Bearer",
            expires_in=self.default_ttl,
            refresh_token=await token.generate(client, subject, rotate=True)
        )
        await self.storage.persist(token)
        return result

    @grant.register
    async def grant_authorization_code(
        self,
        grant: AuthorizationCodeGrant
    ) -> TokenResponse:
        client = grant.get_client()
        _, request = await self.storage.get_code(grant.code)
        if not request.is_authenticated():
            raise TokenException(
                code='invalid_grant',
                description=(
                    "The authorization request was not authorized by the "
                    "Resource Owner."
                )
            )
        subject = await request.get_subject(client, self.subjects)
        if subject is None:
            raise TokenException(code='invalid_grant')
        authorization = await self.storage.get(
            AuthorizationIdentifier(client.client_id, subject.sub)
        )
        if authorization is None:
            raise TypeError("Authorization must exist.")
        assert isinstance(authorization, Authorization)

        request.validate_grant(client, subject, grant)
        self.validate_grant(
            client=client,
            subject=subject,
            grant=grant
        )


        assert subject is not None # nosec
        at = await client.issue_token(
            codec=self.codec,
            using=SIGNING_KEY,
            issuer=self.metadata.issuer,
            audience=grant.get_audience(),
            subject=subject,
            ttl=self.default_ttl,
            scope=request.scope
        )
        await self.storage.delete_authorization_request(request)
        rt = NullRefreshToken()
        if request.wants_refresh_token():
            rt = authorization.create_refresh_token(request.scope)
            await self.storage.persist(rt)

        return TokenResponse(
            access_token=at,
            token_type="Bearer",
            expires_in=self.default_ttl,
            id_token=await self.openid.build(
                signing_key=SIGNING_KEY,
                client=client,
                subject=subject,
                grant=grant,
                scope=request.scope,
                request=request,
                access_token=at
            ),
            state=request.state,
            refresh_token=await rt.generate(client, subject)
        )

    @grant.register
    async def grant_client_credentials(
        self,
        grant: ClientCredentialsGrant
    ) -> TokenResponse:
        # Client credentials grant is only available for confidential
        # clients.
        client = grant.get_client()
        if not client.is_confidential():
            raise InvalidClient(
                error="invalid_client",
                error_description=(
                    "The \"client_credentials\" grant is only available "
                    "for confidential clients."
                )
            )
        if grant.scope is not None and not client.allows_scope(grant.scope):
            raise ForbiddenScope

        # If the request does not include a "resource" parameter, the authorization
        # server MUST use a default resource indicator in the "aud" claim (RFC 9068,
        # Section 3).
        if not grant.resource:
            grant.resource.add(self.metadata.issuer) # type: ignore
        if len(grant.resource) > 1 and not client.can_issue_multiple():
            raise InvalidGrant(
                error_description=(
                    "The client refuses to issue access tokens for multiple "
                    "audiences."
                )
            )
        if not client.allows_audience(self.metadata.issuer, grant.resource):
            raise InvalidGrant(
                error_description=(
                    "The resource(s) specified in the request is not allowed "
                    "by the client."
                )
            )
        return TokenResponse(
            access_token=await client.issue_token(
                codec=self.codec,
                using=SIGNING_KEY,
                issuer=self.metadata.issuer,
                audience=grant.get_audience(),
                subject=client.as_subject(),
                ttl=self.default_ttl,
                scope=set(grant.scope or [])
            ),
            token_type="Bearer",
            expires_in=self.default_ttl,
            id_token=None,
            state=None,
            refresh_token=None
        )

    @grant.register
    async def grant_jwt_bearer(
        self,
        dto: JWTBearerAssertionGrant
    ) -> TokenResponse:
        client = dto.get_client()
        try:
            jws, claims = await self.codec.jwt(dto.assertion)
        except (Malformed, ValueError, TypeError):
            raise InvalidGrant(
                error_description=(
                    "The assertion is malformed and could not be interpreted "
                    "as a JSON Web Token (JWT)."
                )
            )
        claims.verify(
            audience={self.metadata.token_endpoint},
            max_age=self.max_assertion_age,
            required={'iss', 'aud', 'sub', 'iat', 'exp', 'nbf', 'jti'}
        )

        # Check if the assertion is not being replayed.
        if await self.storage.consume(claims):
            raise AssertionReplayed

        # There are two cases that need to be handled here, either the
        # claims are self-signed (a public key is preregistered for the
        # subject specified in the `sub` claim), or the claims were
        # signed by a trusted third-party.
        subject = await self.subjects.get(
            client=client,
            subject_id=typing.cast(int, claims.sub)
        )
        assert subject is not None # nosec
        if dto.scope is not None and not client.allows_scope(dto.scope):
            raise ForbiddenScope
        if not subject.allows_scope(set(dto.scope or [])):
            raise InvalidScope

        # Lookup the JWKS of the issuer as indicated by the `iss` claim,
        # or use the keys pre-registered by the resource owner if the claims
        # are self-signed.
        selfsigned = claims.is_selfsigned()
        if not selfsigned and not self.is_local_issued(claims):
            # The assertion was issued and signed by a third-party.
            if not self.allow_jwks_lookups:
                raise InvalidGrant(
                    error_description=(
                        "The assertion was signed by a third-party, but it's "
                        "public keys are not known to the server and it does "
                        "not allow import using the JWKS URI."
                    )
                )
            if claims.iss not in self.trusted_issuers:
                raise InvalidGrant(
                    error_description=(
                        "The assertion was issued and signed by an issuer that is "
                        "not trusted by the server."
                    )
                )
            raise NotImplementedError
        elif not selfsigned:
            # The assertion was issued and signed by this server.
            raise InvalidGrant(
                error_description=(
                    "The assertion was issued and signed by an issuer that is "
                    "not trusted by the server."
                )
            )
        else:
            verifier = subject

        verified = verifier.verify(jws)
        if inspect.isawaitable(verified):
            verified = await verified
        if not verified:
            raise InvalidGrant(
                error_description=(
                    "The signature of the JWT assertion did not validate. Make "
                    "sure that the signing keys are pre-registered by the "
                    "resource owner."
                )
            )

        # If the request does not include a "resource" parameter, the authorization
        # server MUST use a default resource indicator in the "aud" claim (RFC 9068,
        # Section 3).
        if not dto.resource:
            dto.resource.add(self.issuer) # type: ignore
        if not client.allows_audience(self.issuer, set(dto.resource or [])):
            raise InvalidGrant(
                error_description=(
                    "Any or all of the audiences are not allowed by the client."
                )
            )

        token = await client.issue_token(
            codec=self.codec,
            using=SIGNING_KEY,
            issuer=self.metadata.issuer,
            audience=dto.get_audience(),
            subject=client.as_subject(),
            ttl=self.default_ttl,
            scope=set(dto.scope or [])
        )
        return TokenResponse(
            access_token=token,
            token_type="Bearer",
            expires_in=self.default_ttl,
            id_token=None,
            state=None,
            refresh_token=None
        )

    @grant.register
    async def _grant_session(
        self,
        grant: SessionGrant
    ) -> TokenResponse:
        return await self.grant_session(grant)

    async def grant_session(self, dto: SessionGrant) -> TokenResponse:
        """Grant an access token based on an active user session. The session
        is assumed to be JWE/JWS that are encrypted and/or signed with keys
        known to the authorization server (as specified by the `kid` JOSE
        header claims).
        """
        codec: PayloadCodec = PayloadCodec(
            decrypter=self.keychain,
            verifier=self.keychain
        )
        try:
            data = await codec.decode(dto.session, accept={"jwt+session"})
        except Exception as e:
            self.logger.exception("Caught fatal %s", type(e).__name__)
            self.fail(
                "The authorization server was not able to decrypt "
                "and/or verify the signature of the provided session. "
                "Make sure that the JSON Web Encryption (JWE) and/or "
                "JSON Web Signature (JWS) are created with keys that "
                "are known to the server. Ensure that the `typ` header "
                "claim is equal to 'jwt+session'."
            )
            assert False # nosec
        if not isinstance(data, JSONWebToken):
            self.fail(
                "The authorization server successfully decrypted and/or "
                "verified the signature of the provided token, but it "
                "did not contain a JSON Web Token (JWT)"
            )
            assert False # nosec
        if data.sub is None:
            self.fail("The session did not contain a 'sub' claim.")
            assert False # nosec
        client = dto.get_client()
        subject = await self.subjects.get(
            client=client,
            subject_id=data.sub,
            force_public=True
        )
        if subject is None:
            # If subject is None, then it is not onboarded with the client
            # yet.
            self.logger.info("Subject %s not found.", data.sub)
            subject = await self.issue_pairwise_identifier(self.subjects, client, data.sub)
            assert subject is not None # nosec
            self.logger.info(
                "Onboarded Subject (sub: %s, client: %s, ppid: %s)",
                data.sub, client.client_id, subject.get_identifier(public=False)
            )
        self.validate_grant(client=client, subject=subject, grant=dto)
        self.validate_scope(client=client, subject=subject, grant=dto)
        return TokenResponse(
            access_token=await client.issue_token(
                codec=self.codec,
                using=SIGNING_KEY,
                issuer=self.metadata.issuer,
                audience=dto.get_audience(),
                subject=subject,
                ttl=self.default_ttl,
                scope=set(dto.scope or [])
            ),
            token_type="Bearer",
            expires_in=self.default_ttl,
            id_token=None,
            state=None,
            refresh_token=None
        )

    def validate_scope(
        self,
        client: IClient,
        subject: ISubject | None,
        grant: ScopedGrant
    ) -> None:
        """Validates that the given scope is allowed for the client and subject."""
        if (grant.scope is not None and not client.allows_scope(grant.scope))\
        or (subject is not None and not subject.allows_scope(grant.scope)):
            raise ForbiddenScope

    def validate_grant(
        self,
        client: IClient,
        subject: ISubject | None,
        grant: BaseGrant
    ) -> None:
        """Validates the parameters provided by the grant and sets defaults."""
        # If the request does not include a "resource" parameter, the authorization
        # server MUST use a default resource indicator in the "aud" claim (RFC 9068,
        # Section 3).
        if not grant.resource:
            grant.resource.add(self.issuer) # type: ignore
        if not client.allows_audience(self.issuer, set(grant.resource or [])):
            raise InvalidGrant(
                error_description=(
                    "Any or all of the audiences are not allowed by the client."
                )
            )
        grant.validate_grant(client, subject)

    def fail(self, description: str) -> typing.NoReturn:
        raise InvalidGrant(error_description=description)

    async def issue_pairwise_identifier(
        self,
        subjects: ISubjectRepository,
        client: Any,
        subject_id: Any
    ) -> ISubject:
        """Issue a pairwise identifier for the given :class:`~cbra.ext.oauth2.types.IClient`
        instance, and return a :class:`~cbra.ext.oauth2.types.ISubject` instance.

        Args:
            client (:class:`~cbra.ext.oauth2.types.IClient`): the client for which a token
                is requested.
            subject_id (any): the **public** identifier of a Subject.

        Returns:
            :class:`~cbra.ext.oauth2.types.ISubject`
        """
        raise NotImplementedError