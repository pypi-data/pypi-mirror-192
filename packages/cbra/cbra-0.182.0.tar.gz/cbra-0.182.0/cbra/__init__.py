# pylint: skip-file
import inspect
import typing

from aorta import Command
from aorta import Event
from fastapi import Body
from fastapi import Depends
from fastapi import Header
from fastapi import Request
from fastapi import Path
from fastapi import Query
from fastapi.concurrency import AsyncExitStack
from fastapi.responses import Response
import uvicorn

from .application import Application
from .dependantrunner import DependantRunner
from .dependencyreceiver import DependencyReceiver
from .endpoint import Endpoint
from .endpointmetaclass import EndpointMetaclass
from .injectedmessagehandler import CommandHandler
from .injectedmessagehandler import EventListener
from .options import Options
from .resource import Resource
from .useragent import UserAgent
from . import cors
from . import renderers
from . import transaction
from . import types
from . import utils
from . import query


__all__ = [
    'cors',
    'renderers',
    'run',
    'transaction',
    'query',
    'summary',
    'types',
    'utils',
    'Application',
    'Body',
    'Command',
    'CommandHandler',
    'Depends',
    'DependantRunner',
    'DependencyReceiver',
    'Endpoint',
    'EndpointMetaclass',
    'Event',
    'EventListener',
    'Header',
    'Options',
    'Path',
    'Query',
    'Resource',
    'Response',
    'UserAgent',
]


def run(
    app: typing.Union[str, Application],
    *args: typing.Any,
    **kwargs: typing.Any
):
    """Like :func:`uvicorn.run`, but with additional integrations with
    :mod:`cbra`.
    """
    from cbra.conf import settings
    kwargs.setdefault('ssl_certfile', settings.LOCALHOST_SSL_CRT)
    kwargs.setdefault('ssl_keyfile', settings.LOCALHOST_SSL_KEY)
    return uvicorn.run(app, *args, **kwargs)


def description(value: str) -> typing.Callable[..., typing.Any]:
    """Set the OpenAPI response description for a request handler."""
    def decorator(
        func: typing.Callable[..., typing.Any]
    ) -> typing.Callable[..., typing.Any]:
        setattr(func, "response_description", value)
        return func
    return decorator


def summary(value: str) -> typing.Callable[..., typing.Any]:
    """Set the OpenAPI summary for a request handler."""
    def decorator(
        func: typing.Callable[..., typing.Any]
    ) -> typing.Callable[..., typing.Any]:
        setattr(func, "summary", value)
        return func
    return decorator


async def run_dependant(
    app: Application,
    dependant: typing.Callable,
    scope: dict = {},
    path: str = None
):
    """Run callable `dependant` and ensure that it is invoked with all its
    dependencies resolved.
    """
    runner = DependantRunner()
    async with AsyncExitStack() as stack:
        request = Request(
            scope={
                'app': app,
                'type': "http",
                'query_string': '',
                'headers': [
                    (b'host', b'foo.bar.baz')
                ],
                'fastapi_astack': stack,
                **scope
            }
        )
        result = runner.run_dependant(request, dependant, path=path)
        if inspect.isawaitable(result):
            result = await result

    return result
