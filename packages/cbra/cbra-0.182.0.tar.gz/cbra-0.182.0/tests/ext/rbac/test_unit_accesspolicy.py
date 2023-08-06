# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.rbac.types import AccessPolicy
from cbra.ext.rbac import BaseAuthorizationContext


policy: AccessPolicy = AccessPolicy.parse_obj({
    'bindings': [
        {'role': 'owner', 'members': [
            'user:cochise.ruhulessin@unimatrixone.io',
            'client:test@oauth2.unimatrixapis.com'
        ]},
        {'role': 'editor', 'members': ['user:c.ruhulessin@molano.nl']},
        {'role': 'client', 'members': ['client:test@oauth2.unimatrixapis.com']},
    ]
})


def test_match_user():
    ctx: BaseAuthorizationContext = BaseAuthorizationContext(
        issuer='python-cbra.dev.unimatrixone.io',
        subject='1',
        email='cochise.ruhulessin@unimatrixone.io',
        client_id='test'
    )
    result = policy.match(ctx)
    assert result.has('owner')
    assert not result.has('editor')
    assert not result.has('client')


def test_match_client():
    ctx: BaseAuthorizationContext = BaseAuthorizationContext(
        issuer='oauth2.unimatrixapis.com',
        subject='test',
        client_id='test'
    )
    result = policy.match(ctx)
    assert result.has('client')
    assert result.has('owner')
    assert not result.has('editor')