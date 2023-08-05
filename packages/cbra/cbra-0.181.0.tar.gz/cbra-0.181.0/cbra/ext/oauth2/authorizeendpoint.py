"""Declares :class:`AuthorizationEndpoint`."""
import datetime
import typing
import urllib.parse
from typing import Any

import fastapi

from cbra.types import IPrincipal
from ckms.jose import PayloadCodec
from .authorization import Authorization
from .authorizationrequestclient import AuthorizationRequestClient
from .endpoint import Endpoint
from .exceptions import CrossOriginNotAllowed
from .exceptions import Error
from .exceptions import LoginRequired
from .params import CurrentServerMetadata
from .params import DownstreamProvider
from .params import LocalIssuer
from .params import OIDCTokenBuilder
from .params import Server
from .params import ServerCodec
from .params import SubjectRepository
from .params import TransientStorage
from .params import UpstreamProvider
from .requestobjectdecoder import RequestObjectDecoder
from .types import AuthorizationException
from .types import AuthorizationIdentifier
from .types import AuthorizationRequest
from .types import AuthorizationRequestParameters
from .types import IAuthorizationServer
from .types import IAuthorizeEndpoint
from .types import IClient
from .types import IStorage
from .types import ISubject
from .types import ISubjectRepository
from .types import IUpstreamProvider
from .types import JAR
from .types import IOIDCTokenBuilder
from .types import ServerMetadata


class AuthorizationEndpoint(Endpoint, IAuthorizeEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    codec: PayloadCodec = ServerCodec
    summary: str = "Authorization Endpoint"
    decoder: RequestObjectDecoder
    denied_url: str
    description: str = (
        "The **Authorization Endpoint** is used to interact with the resource "
        "owner and obtain an authorization grant."
    )
    login_endpoint: str | None
    login_url: str | None
    metadata: ServerMetadata = CurrentServerMetadata
    methods: set[str] = {"GET"}
    query_model: type[AuthorizationRequestParameters] = AuthorizationRequestParameters
    require_authentication: bool = False
    openid: IOIDCTokenBuilder = OIDCTokenBuilder
    options_description: str = (
        "Communicates the allowed methods and CORS options for "
        "the **Authorization Request** endpoint."
    )
    prompt_url: str
    provider: IUpstreamProvider | None

    def __init__(
        self,
        decoder: RequestObjectDecoder = fastapi.Depends(),
        issuer: str = LocalIssuer,
        server: IAuthorizationServer = Server,
        storage: IStorage = TransientStorage,
        subjects: ISubjectRepository = SubjectRepository,
        provider: IUpstreamProvider | None = UpstreamProvider
    ):
        self.decoder = decoder
        self.issuer = issuer
        self.login_url = server.login_url
        self.login_endpoint = server.login_endpoint
        self.provider = provider
        self.storage = storage
        self.subjects = subjects

    @staticmethod
    async def callback(
        request: fastapi.Request,
        provider: IUpstreamProvider = DownstreamProvider,
        storage: IStorage = TransientStorage
    ) -> fastapi.Response:
        """Return path for upstream identity providers."""
        return await provider.on_return(storage, request)

    async def add_to_client(
        self,
        client: IClient,
        principal: IPrincipal,
        dto: AuthorizationRequest
    ) -> ISubject:
        """Add the principal given its subject identifier to the client. This
        method is invoked when handling an authorization request for a client
        with which a subject has never authenticated before.
        """
        await self.onboard(client, principal, dto)
        return await self.subjects.persist(client, principal)

    async def onboard(
        self,
        client: Any,
        principal: Any,
        dto: AuthorizationRequest
    ) -> None:
        """Onboard the Subject with the Client. The default implementation
        does nothing; subclasses may override this method in order to provide
        customized onboarding policies.
        """
        pass

    async def create_redirect(
        self,
        client: IClient,
        dto: AuthorizationRequest
    ) -> str:
        """Return the redirect URI for a previously validated
        :class:`AuthorizationRequest`.
        """
        if self.provider is not None:
            return await self.create_upstream_redirect(dto=dto)

        redirect_uri = None
        assert dto.redirect_uri is not None # nosec
        assert bool(dto.authorization_code) # nosec
        redirect_uri = await dto.redirect_uri.authorize(
            client=client,
            metadata=self.metadata,
            response_mode=dto.get_response_mode(),
            codec=await client.get_codec(self.codec),
            code=dto.authorization_code,
            iss=self.issuer,
            state=dto.state
        )
        assert redirect_uri is not None # nosec
        return redirect_uri

    async def create_upstream_redirect(
        self,
        dto: AuthorizationRequest
    ) -> str:
        """Return a string containing the redirection endpoint at the
        upstream identity provider.
        """
        assert self.provider is not None # nosec
        return await self.provider.create_redirect(self.request, dto) # type: ignore

    async def enforce_policy(
        self,
        dto: AuthorizationRequest,
        client: IClient,
        subject: ISubject
    ) -> None:
        """Enforces the access policy for the given client and subject."""
        failures: list[AuthorizationException] = []
        if dto.claims:
            claims = self.openid.parse_claims(dto.claims)
            errors = await self.openid.enforce_claims(
                dto, client, subject, claims.id_token
            )
            failures.extend(errors) # type: ignore
        for error in failures:
            error.log(self.logger)
        if failures:
            self.deny(dto, failures[0])

    async def enforce_cors_policy( # type: ignore
        self,
        params: AuthorizationRequestParameters = fastapi.Depends(),
        client: IClient = AuthorizationRequestClient,
        origin: str | None = fastapi.Header(
            default=None,
            alias='Origin'
        )
    ):
        if not client.allows_origin(origin):
            raise CrossOriginNotAllowed(
                redirect_uri=client.get_redirect_url(
                    url=params.redirect_uri,
                    fatal=False
                ),
                state=params.state
            )

    async def get_subject(
        self,
        client: IClient,
        principal: IPrincipal,
        dto: AuthorizationRequest
    ) -> ISubject | None:
        """Return a :class:`~cbra.ext.oauth2.types.ISubject` instance
        representing the currently authenticated principal.
        """
        subject = await dto.get_subject(client, self.subjects)
        if subject is None:
            # There was no credential attached to the authorization request
            # that could identify the subject.
            subject = await self.subjects.get(
                client=client,
                subject_id=principal.sub,
                force_public=True
            ) or await self.add_to_client(client, principal, dto)
        assert subject is not None
        if subject and principal and (subject.sub != principal.sub):
            self.logger.critical(
                "Principal does not authenticate the Subject "
                "(principal: %s, subject: %s)",
                self.principal.sub, subject.sub
            )
            raise Error(
                error="invalid_request",
                error_description=(
                    "The authenticated subject does not match the subject "
                    "for which the authorization request was created."
                ),
                mode='client'
            )
        return subject

    async def resolve(
        self,
        client: IClient,
        params: AuthorizationRequestParameters
    ) -> AuthorizationRequest:
        """Inspect the authorization request and determine if it
        needs to be retrieved from the storage or an external source,
        if the `request` or `request_uri` parameters are provided.
        Otherwise return the request.
        """
        if params.request and params.request_uri:
            raise Error(
                error_description=(
                    "An authorization request can not include both the "
                    "\"request\" and \"request_uri\" parameters."
                )
            )
        if params.is_object():
            # A Request Object as specified in RFC 9101
            assert params.request is not None
            claims = await self.decoder.decode_request_object(params.request)
            return AuthorizationRequest.fromparams(JAR(**claims))

        if not params.is_reference():
            return AuthorizationRequest.fromparams(params)
        if params.is_external():
            raise Error(
                error="invalid_request_uri",
                error_description=(
                    "The application does not allow retrieving authorization "
                    "request parameters from the uri that was provided with "
                    "the \"request_uri\" parameter."
                )
            )

        assert params.request_id is not None # nosec
        request = await self.storage.get_authorization_request(params.request_id)
        if request.client_id != client.client_id:
            self.logger.critical(
                "Authorization request (id: %s) was not issued by client %s",
                request.request_id, client.client_id
            )
            raise Error(
                error="invalid_request",
                error_description="The authorization request was not valid."
            )
        return request

    async def handle(
        self,
        client: IClient = AuthorizationRequestClient,
        params: AuthorizationRequestParameters = fastapi.Depends()
    ) -> fastapi.responses.Response:
        """Initiates the **Authorization Code Flow**."""
        request: None | AuthorizationRequest = None
        try:
            request = await self.resolve(client, params)
            return await self.get_redirect_response(client, request)
        except Exception as e:
            return await self.on_fatal_exception(client, request, e)

    async def on_fatal_exception(
        self,
        client: Any,
        request: Any | None,
        e: Exception
    ) -> fastapi.responses.Response:
        """Hook that is invoked when a fatal exception occurs during the authorization
        flow.
        """
        raise

    async def get_authorization(
        self,
        client_id: int | str,
        sub: int | str
    ) -> Authorization:
        """Return the :class:`~cbra.ext.oauth2.Authorization` that is
        granted to the Client by the Resource Owner. If the Client did
        not obtain any grant previously, return the object without any
        scopes.
        """
        key = AuthorizationIdentifier(client_id=client_id, sub=sub)
        authorization = await self.storage.get(key)
        if authorization is None:
            authorization = Authorization.fromkey(key)
        assert isinstance(authorization, Authorization) # nosec
        return authorization

    async def get_redirect_response(
        self,
        client: IClient,
        dto: AuthorizationRequest
    ) -> fastapi.responses.Response:
        """Initiates the **Authorization Code Flow**."""
        if not self.principal.is_authenticated():
            await self.on_login_required(dto)
            assert False # nosec
        subject = await self.get_subject(
            client=client,
            principal=self.principal,
            dto=dto
        )
        assert self.principal.sub is not None # nosec
        assert subject is not None # nosec
        authorization = await self.get_authorization(
            client.client_id,
            self.principal.sub
        )

        # Check if the request parameters are valid.
        await self.validate_request(
            client=client,
            subject=subject,
            dto=dto
        )

        # Check if the subject allows the scope requested. If the subject
        # does not allow the scope requested, redirect to the consent_url
        # or present a page when the subject can allow the scope.
        if not client.is_first_party() and not subject.allows_scope(dto.scope):
            return self.redirect_consent(dto)

        # Handle scope and claims parameters. Run handlers to determine
        # if we need additional information from the subject (TODO).

        redirect_uri = await self.create_redirect(client, dto=dto)
        dto.auth_time = self.principal.get_auth_time()
        assert dto.sub is not None
        try:
            await self.validate(dto, client, subject, self.principal)
            await self.enforce_policy(
                dto=dto,
                client=client,
                subject=subject
            )
            await self.on_success(dto, client, subject)

            # TODO: The scope should be accepted out of band.
            now = datetime.datetime.utcnow()
            for scope in dto.scope:
                authorization.authorize(scope, now=now)
            if dto.allows_refresh():
                authorization.enable_refresh()
        finally:
            await self.persist(dto)
            await self.persist(authorization)
        return fastapi.responses.RedirectResponse(
            url=redirect_uri,
            status_code=303
        )

    async def on_success(
        self,
        dto: Any,
        client: Any,
        subject: Any
    ) -> None:
        """Invoked when the authorization request can successfully
        proceed.
        """
        pass

    async def validate(
        self,
        dto: AuthorizationRequest,
        client: typing.Any,
        subject: ISubject,
        principal: typing.Any
    ) -> None:
        """Validates the authorization request with regards to the currently
        authenticated subject. This method is expected to raise an exception
        if, for whatever reason, the authorization request can not continue.

        At this point, the authorization request may be considered valid and
        any error condition may trigger a redirect back to the client
        appication. If there are configuration errors that can not redirect,
        such as an invalid redirect URI, these are handled prior to the
        invocation of :meth:`validate()`.
        """
        pass

    async def on_login_required(self, dto: AuthorizationRequest):
        """Raises an exception indicating that authentication is required."""
        if dto.is_openid() and not dto.can_interact():
            raise Error(
                error="login_required",
                error_description=(
                    "Provide credentials using the designated mechanisms."
                ),
                mode='redirect'
            )

        if self.login_endpoint:
            raise NotImplementedError

        if self.login_url:
            raise LoginRequired(
                redirect_to=self.login_url,
                params={
                    **self.get_url_params(dto),
                    'next': self.get_current_url(dto)
                }
            )

    def deny(
        self,
        dto: AuthorizationRequest,
        error: AuthorizationException
    ) -> typing.NoReturn:
        """Denies the authorization request. If the request is able to interact
        with the end-user, prompt the user displaying the reason. Otherwise,
        display a generic message.
        """
        if dto.can_interact():
            assert self.login_url is not None # nosec
            error.raise_for_user(self.denied_url, dto.redirect_uri)
        raise NotImplementedError("Can not interact")

    def interact(self, dto: AuthorizationRequest) -> typing.NoReturn:
        """Interact with the end-user."""
        if not self.login_url:
            raise ValueError("AuthorizeEndpoint.login_url is not configured.")
        raise LoginRequired(
            redirect_to=self.login_url,
            params={'next': self.get_current_url(dto)}
        )

    def get_current_url(self, dto: AuthorizationRequest) -> str:
        """Ensure that the URL is always the same as the authorization
        endpoint listed in the server metadata.
        """
        p = urllib.parse.urlparse(self.metadata.authorization_endpoint)
        url = self.request.url.replace(netloc=p.netloc)
        return str(url)

    def get_url_params(self, dto: AuthorizationRequest) -> dict[str, str]:
        q: dict[str, str] = {}
        # Set some query parameters from the authorization request. This
        # should never include PII.
        if dto.ui_locales:
            q['ui_locales'] = str.join(' ', dto.ui_locales)
        return q

    async def persist(
        self,
        dto: AuthorizationRequest | Authorization
    ) -> None:
        """Inspect the request parameters and persist the appropriate
        objects to the transient storage.
        """
        await self.storage.persist(dto)
        if isinstance(dto, AuthorizationRequest)\
        and dto.needs_authorization_code():
            await self.storage.persist(dto.get_authorization_code())

    def redirect_consent(self, dto: AuthorizationRequest) -> fastapi.Response:
        """Create a response that redirects the user-agent to a
        page where the resource owner can grant consent to the
        client.
        """
        if dto.is_openid() and not dto.can_interact():
            raise Error(
                error="consent_required",
                error_description=(
                    "The resource owner has not granted consent to this client "
                    "for the requested scope, and the authorization server "
                    "was instructed not to prompt the resource owner with an "
                    "interface to obtain consent.\n\n"
                    "This indicates a misconfiguration. Contact your system "
                    "administrator or support department for further "
                    "information."
                )
            )
        raise NotImplementedError
        
    async def validate_request(
        self,
        client: IClient,
        subject: ISubject,
        dto: AuthorizationRequest
    ) -> None:
        """Validates an OAuth 2.0 authorization request."""
        await dto.validate_request_parameters(
            client=client,
            subject=subject,
            openid=self.openid
        )
        dto.sub = typing.cast(str, subject.sub)