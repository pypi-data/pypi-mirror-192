"""Declares :class:`TokenRequestHandler`."""
import typing

import fastapi
from ckms.types import WrongAudience
from unimatrix.exceptions import CanonicalException

from .endpoint import Endpoint
from .exceptions import CrossOriginNotAllowed
from .exceptions import Error
from .exceptions import InvalidGrant
from .params import Server
from .params import ServerTokenIssuer
from .tokenissuer import TokenIssuer
from .tokenrequest import TokenRequest
from .types import BaseGrant
from .types import IAuthorizationServer
from .types import TokenException
from .types import TokenResponse


class TokenRequestHandler(Endpoint):
    __module__: str = 'cbra.ext.oauth2'
    response_model: typing.Type[TokenResponse] = TokenResponse
    methods: set[str] = {"POST"}
    name: str = 'oauth2.token'
    summary: str = "Token Endpoint"
    description: str = (
        "The **Token Endpoint** is used by an application in order to "
        "get an access token or a refresh token. It is used by all "
        "flows except for the *Implicit Flow* because in that case an "
        "access token is issued directly.\n\n"
        "Depending on the client, the `Authorization` header or "
        "the `client_id` and `client_secret` body parameters may be "
        "mandatory to authenticate a confidential client."
    )

    #: Description for the OPTIONS request handler.
    options_description: str = (
        "Communicates the allowed methods and CORS options for "
        "the **Token Endpoint**."
    )

    #: The parameters provided with the token request.
    params: BaseGrant

    def __init__(
        self,
        params: BaseGrant = TokenRequest
    ):
        self.params = params

    async def enforce_cors_policy(
        self,
        origin: str | None = fastapi.Header(
            default=None,
            alias='Origin'
        )
    ):
        client = self.params.get_client()
        if origin and not client.allows_origin(origin):
            raise CrossOriginNotAllowed(model='client')

    async def handle(
        self,
        server: IAuthorizationServer = Server,
        issuer: TokenIssuer = ServerTokenIssuer
    ) -> dict[str, typing.Any]:
        """Invokes the :attr:`TokenRequestHander.issuer` with the
        given grant type and return the result to the client.
        """
        if not server.allows_grant(self.params.grant_type.value):
            raise InvalidGrant(
                error_description=(
                    "The server does not allow use of the grant \""
                    f"{self.params.grant_type}\"."
                ),
                mode='client'
            )
        return (await issuer.grant(self.params))\
            .dict(exclude_defaults=True, exclude_none=True)

    async def on_exception( # type: ignore
        self,
        exception: Exception
    ) -> fastapi.Response:
        if isinstance(exception, WrongAudience):
            raise Error(
                error="invalid_grant",
                error_description=(
                    "The audience of the supplied JWT was not accepted "
                    "by the server."
                )
            )
        elif isinstance(exception, CanonicalException):
            raise Error(
                error="server_error",
                error_description=exception.message
            )
        elif isinstance(exception, TokenException):
            raise
        self.logger.exception("Caught fatal %s", type(exception).__name__)
        return fastapi.responses.JSONResponse(
            status_code=400,
            content={
                'error': 'server_error',
                'error_description': (
                    "The authorization server encountered an error condition "
                    "from which it was unable to recover."
                )
            }
        )