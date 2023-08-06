# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

import aorta


class ISagaRepository:
    pass


T = TypeVar('T', bound='Saga')


class EventA(aorta.Event):
    order_id: int


import functools

class EventB(aorta.Event):
    order_id: int


class EventC(aorta.Event):
    warehouse_order_id: int


from typing import Generic

T = TypeVar('T')




import functools

class handler:
    events: dict[type[aorta.Event], None] = {}

    def __init__(self, init):
        self.events = {}
        self.init = init

    def on_event(self, event: type[aorta.Event]):
        def decorator_factory(func):
            self.events[event._model] = func
            def f(self, *args, **kwargs):
                return func(self, *args, **kwargs)
            f.on_event = self.on_event
            return f
        return decorator_factory

    def __call__(self, event: type[aorta.Event]):
        return self.events[type(event._params)](saga, event)


class Saga:
    fulfillment_id: int
    tracking_code: str | None
    order_id: int
    warehouse_order_id: int | None

    @handler
    def handle(self, event: EventA | EventB | EventC):
        pass

    @handle.on_event(EventA)
    def handle(self, event: EventA):
        return 'Event A!'