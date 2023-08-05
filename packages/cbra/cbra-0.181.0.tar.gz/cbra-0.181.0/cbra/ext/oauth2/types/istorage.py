"""Declares :class:`IStorage`."""
import functools
import typing
from typing import Any

from ckms.types import ClaimSet

from ..exceptions import Error
from .authorizationcode import AuthorizationCode
from .authorizationidentifier import AuthorizationIdentifier
from .authorizationrequest import AuthorizationRequest
from .baseauthorizationrequest import BaseAuthorizationRequest
from .iauthorization import IAuthorization
from .irefreshtoken import IRefreshToken
from .refreshtokenidentifier import RefreshTokenIdentifier


class IStorage:
    """Declares the interface that storage implementations for the OAuth 2.0
    server need to implement.
    """
    __module__: str = 'cbra.ext.oauth2.types'
    InvalidAuthorizationCode: type[Error] = type('InvalidAuthorizationCode', (Error, ), {
        'error': "invalid_grant",
        'error_description': "The presented authorization code grant is not valid."
    })

    async def consume(self, claims: ClaimSet) -> bool:
        """Consume the claims set, ensuring that its token can only be
        used once. Return a boolean indicating if the token was already
        consumed.
        """
        raise NotImplementedError

    async def delete_authorization_request(self, request: Any) -> None:
        """Delete the provided authorization request"""
        raise NotImplementedError

    @functools.singledispatchmethod
    async def get(
        self,
        key: AuthorizationIdentifier | RefreshTokenIdentifier
    ) -> Any:
        """Return a key from the transient storage backend, or ``None``
        if it does not exist.
        """
        raise NotImplementedError

    @get.register
    async def _get_authorization_by_natural_key(
        self,
        key: AuthorizationIdentifier
    ) -> Any:
        return await self.get_authorization_by_natural_key(key.client_id, key.sub)

    @get.register
    async def _get_refresh_token_by_id(
        self,
        key: RefreshTokenIdentifier
    ) -> IRefreshToken | None:
        return await self.get_refresh_token_by_id(key)

    async def get_authorization_by_natural_key(
        self,
        client_id: int | str,
        subject_id: int | str
    ) -> Any:
        raise NotImplementedError

    async def get_authorization_request(
        self,
        request_id: str
    ) -> AuthorizationRequest:
        """Lookup an authorization request from the transient storage."""
        raise NotImplementedError

    async def get_code(self, code: str) -> tuple[AuthorizationCode, AuthorizationRequest]:
        """Lookup an authorization code."""
        raise NotImplementedError

    async def get_pushed_authorization_request(
        self,
        request_uri: str
    ) -> BaseAuthorizationRequest:
        """Look an authorization request that was pushed through the Pushed
        Authorization Request (PAR) endpoint.
        """
        raise NotImplementedError

    async def get_refresh_token_by_id(
        self,
        key: RefreshTokenIdentifier
    ) -> IRefreshToken | None:
        """Return the :class:`~cbra.ext.oauth2.types.IRefreshToken` by its
        identifier `key`.
        """
        raise NotImplementedError

    async def set(
        self,
        key: str,
        value: typing.Union[bytes, str],
        expires: typing.Optional[int] = None
    ) -> None:
        """Set a `key` to given `value` to the **transient** storage backend.
        If `value` is a :class:`dict`, then all its members must be
        JSON-serializable.

        The `expires` parameter define the period after which the key expires
        i.e. it should be (automatically) removed from the transient storage
        backend. It is denoted in seconds.
        """
        raise NotImplementedError

    @functools.singledispatchmethod
    async def persist(
        self,
        obj: AuthorizationRequest | AuthorizationCode | IAuthorization | IRefreshToken
    ) -> None:
        """Persist an object to the transient storage."""
        raise NotImplementedError(type(obj).__name__)

    @persist.register
    async def _persist_authorization(
        self,
        obj: IAuthorization
    ) -> None:
        return await self.persist_authorization(obj)

    @persist.register
    async def _persist_authorizationcode(
        self,
        obj: AuthorizationCode
    ) -> None:
        return await self.persist_authorizationcode(obj)

    @persist.register
    async def _persist_authorizationrequest(
        self,
        obj: AuthorizationRequest
    ) -> None:
        return await self.persist_authorizationrequest(obj)

    @persist.register
    async def _persist_refresh_token(
        self,
        obj: IRefreshToken
    ) -> None:
        return await self.persist_refresh_token(obj)

    async def persist_authorization(
        self,
        obj: IAuthorization
    ) -> None:
        raise NotImplementedError

    async def persist_authorizationcode(
        self,
        obj: AuthorizationCode
    ) -> None:
        """Persist an :class:`cbra.ext.oauth2.types.AuthorizationCode`
        instance.
        """
        raise NotImplementedError

    async def persist_authorizationrequest(
        self,
        obj: AuthorizationRequest
    ) -> None:
        """Persist an :class:`cbra.ext.oauth2.AuthorizationRequest`
        instance.
        """
        raise NotImplementedError

    async def persist_refresh_token(
        self,
        obj: IRefreshToken
    ) -> None:
        """Persist an :class:`cbra.ext.oauth2.types.IRefreshToken`
        instance.
        """
        raise NotImplementedError

    async def pop(
        self,
        key: str
    ) -> typing.Optional[typing.Union[bytes, str]]:
        """Like :meth:`get()`, but also removes the key."""
        raise NotImplementedError