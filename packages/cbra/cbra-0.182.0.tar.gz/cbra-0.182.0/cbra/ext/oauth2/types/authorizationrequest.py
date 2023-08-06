"""Declares :class:`AuthorizationRequest`."""
import secrets
import typing
from typing import Any

import pydantic
from ckms.types import JSONWebKey

from ..exceptions import ClientUnsupportedResponseMode
from ..exceptions import Error
from ..exceptions import ForbiddenScope
from ..exceptions import InvalidGrant
from ..exceptions import UnsupportedResponseMode
from ..exceptions import UnsupportedResponseType
from .accesstype import AccessType
from .authorizationidentifier import AuthorizationIdentifier
from .authorizationcode import AuthorizationCode
from .authorizationcodegrant import AuthorizationCodeGrant
from .authorizationrequestparameters import AuthorizationRequestParameters
from .iclient import IClient
from .isubject import ISubject
from .isubjectrepository import ISubjectRepository
from .iopenidtokenbuilder import IOpenIdTokenBuilder as OIDCHandler
from .redirecturl import RedirectURL
from .responsetype import ResponseType
from .jar import JAR
from .servermetadata import ServerMetadata
from .tokenexception import TokenException


DEFAULT_RESPONSE_MODES: dict[str, str] = {
    ResponseType.code.value: 'query',
    ResponseType.code_id_token: 'fragment',
    ResponseType.code_id_token_token: 'fragment',
    ResponseType.code_token: 'fragment',
    ResponseType.id_token: 'fragment',
    ResponseType.id_token_token: 'fragment',
    ResponseType.none: 'fragment',
    ResponseType.token: 'fragment',
}


class AuthorizationRequest(pydantic.BaseModel):
    """Represents the cleaned parameters of an authorization request."""
    __module__: str = 'cbra.ext.oauth2.types'

    #: Identifies the request. Is used in both Pushed Authorization Requests
    #: (PAR), as well as the `state` parameter (or similar) when the
    #: authorization server redirects the user-agent to an upstream identity
    #: provider. This attribute must never be set manually.
    request_id: str

    #: If the Authorization Code Flow is used, the authorization code that the
    #: client may used to obtain an access token.
    authorization_code: str = pydantic.Field(default='')

    client_id: str
    response_type: ResponseType | None
    redirect_uri: RedirectURL
    scope: set[str]
    state: str | None
    access_type: AccessType

    # The Response Mode determines how the Authorization Server returns
    # result parameters from the Authorization Endpoint. Non-default
    # modes are specified using the response_mode request parameter.
    # If response_mode is not present in a request, the default Response
    # Mode mechanism specified by the Response Type is used.
    # (OAuth 2.0 Multiple Response Type Encoding Practices)
    response_mode: str | None
    resource: set[str]
    nonce: str | None
    display: str | None
    prompt: str | None
    max_age: int | None
    ui_locales: list[str]
    claims_locales: list[str]
    id_token_hint: str | None
    login_hint: str | None
    acr_values: set[str]
    amr_values: set[str]
    registration: str | None
    claims: dict[str, Any] | None

    # Extensions
    access_token: str | None
    id_token: str | None
    encryption_key: JSONWebKey | None

    # Internal
    auth_time: int | None = None
    sub: str | int | None = None
    redirect_uri_provided: bool
    session: dict[str, Any] = {}
    artifacts: dict[str, Any] = {}

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        response_mode = values.get('response_mode')
        response_type = values.get('response_type')
        if response_type and not response_mode:
            # Set the default response mode for the response type if it was
            # not defined by the client.
            values['response_mode'] = DEFAULT_RESPONSE_MODES[response_type]
        return values

    @classmethod
    def fromparams(
        cls,
        params: AuthorizationRequestParameters | JAR
    ) -> 'AuthorizationRequest':
        """Create a new :class:`AuthorizationRequest` from the parameters 
        provided to the :term:`Authorization Endpoint` or :term:`PAR Endpoint`.
        """
        return cls(
            request_id=secrets.token_urlsafe(24),
            client_id=params.client_id,
            response_type=params.response_type,
            redirect_uri=params.get_redirect_url(),
            scope=params.get_scope(),
            state=params.state,
            access_type=params.access_type,
            response_mode=params.response_mode,
            resource=params.get_resources(),
            nonce=params.nonce,
            display=params.display,
            prompt=params.prompt,
            max_age=params.max_age,
            ui_locales=params.get_ui_locales(),
            claims_locales=params.get_claims_locales(),
            id_token_hint=params.id_token_hint,
            login_hint=params.login_hint,
            acr_values=params.get_acr_values(),
            amr_values=params.get_amr_values(), # type: ignore
            registration=params.registration,
            claims=params.get_claims(),
            access_token=None,
            id_token=None,
            encryption_key=None,
            redirect_uri_provided=bool(params.redirect_uri)
        )

    def __init__(self, **kwargs: typing.Any):
        super().__init__(**kwargs)
        if self.needs_authorization_code():
            self.authorization_code = secrets.token_urlsafe(48)

    #def authorize(self):
    #    """Authorize the request and return a string containing the
    #    redirect URL.
    #    """
    #    params = {
    #        'code': self.authorization_code
    #    }
    #    if self.state is not None:
    #        params['state'] = self.state
    #    assert self.redirect_uri is not None # nosec
    #    return self.redirect_uri.authorize(**params)

    def allows_refresh(self) -> bool:
        """Return a boolean if refresh tokens are requested."""
        return self.access_type == AccessType.offline

    def can_interact(self) -> bool:
        """Return a boolean indicating if the authorization server or its
        delegated can interact with the resource owner.
        """
        return self.prompt != "none"

    def get_authorization_code(self) -> AuthorizationCode:
        """Return the authorization code."""
        if not self.needs_authorization_code():
            raise ValueError("Invalid response type for authorization code.")
        return AuthorizationCode(
            request_id=self.request_id,
            code=self.authorization_code
        )

    async def get_subject(
        self,
        client: IClient,
        subjects: ISubjectRepository
    ) -> ISubject | None:
        """Return the subject instance, if the authorization request provided
        credentials."""
        if not self.is_authenticated():
            return None
        if self.id_token or self.access_token:
            raise NotImplementedError
        return await subjects.get(client, self.sub, force_public=True)

    def get_response_mode(self) -> str:
        """Return the response mode defined by the request, or default to the response
        mode for the given response type.
        """
        return self.response_mode or 'query'

    def is_authenticated(self) -> bool:
        """Return a boolean indicating if the request was authenticated using
        the :attr:`id_token` or :attr:`access_token` parameters.
        """
        return bool(self.id_token or self.access_token or self.sub)

    def is_openid(self) -> bool:
        """Return a boolean indicating if the authorization request is
        an OpenID Connect request.
        """
        return "openid" in self.scope

    def needs_authorization_code(self) -> bool:
        """Return a boolean indicating if the authorization code flow
        is used.
        """
        return self.response_type in {
            ResponseType.code,
            ResponseType.code_id_token,
            ResponseType.code_id_token_token,
            ResponseType.code_token
        }

    def validate_grant(
        self,
        client: IClient,
        subject: ISubject | None,
        grant: AuthorizationCodeGrant
    ) -> None:
        # The "redirect_uri" parameter is required "if the "redirect_uri"
        # parameter was included in the authorization request as described
        # in Section 4.1.1, and their values MUST be identical."
        # (RFC 6749, 4.1.3)
        if self.redirect_uri_provided and not grant.redirect_uri:
            raise TokenException(
                code='invalid_grant',
                description=(
                    "The authorization request specified the \"redirect_uri\" "
                    "parameter, thus the token request must include the "
                    "same parameter with an identical value."
                )
            )
        if str(self.redirect_uri) != grant.redirect_uri:
            raise TokenException(
                code='invalid_grant',
                description=(
                    "The \"redirect_uri\" parameter must be identical to the "
                    "value provided in the authorization request."
                )
            )

    async def validate_request_parameters(
        self,
        *,
        client: IClient,
        subject: ISubject | None,
        openid: OIDCHandler,
        metadata: ServerMetadata | None = None
    ):
        """Validates the authorization request."""
        if self.response_type is None:
            raise Error(
                error="invalid_request",
                error_description="The response_type parameter is required."
            )
        self.redirect_uri = typing.cast(
            RedirectURL,
            client.get_redirect_url(self.redirect_uri)
        )
        if not client.allows_response_type(self.response_type):
            raise UnsupportedResponseType.as_redirect(self.redirect_uri)
        if not client.allows_response_mode(self.response_mode):
            raise ClientUnsupportedResponseMode.as_redirect(self.redirect_uri)
        if not client.allows_scope(self.scope):
            raise ForbiddenScope
        if metadata is not None:
            if not metadata.supports_response_mode(self.response_mode):
                raise UnsupportedResponseMode.as_redirect(self.redirect_uri)

        if self.claims and not openid.validate_claims(self.claims):
            raise Error(
                error="invalid_request",
                error_description="Invalid claims parameter."
            )

    def wants_amr(self, value: str | set[str]) -> bool:
        """Return a boolean indicating if this request requires the
        given Authentication Method Reference (AMR) value(s).
        """
        if isinstance(value, str):
            value = {value}
        return bool(value & set(self.amr_values))

    def wants_refresh_token(self) -> bool:
        """Return a boolean indicating if the authorization request
        wants a refresh token.
        """
        return self.access_type == AccessType.offline