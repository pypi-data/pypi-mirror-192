# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.rbac.types import ClientPrincipal
from cbra.ext.rbac.types import UserPrincipal


def test_hash_client():
    principals = {
        ClientPrincipal(issuer='foo', client_id='bar'),
        ClientPrincipal(issuer='foo', client_id='bar'),
    }
    assert len(principals) == 1


def test_hash_user():
    principals = {
        UserPrincipal('foo@bar.baz'),
        UserPrincipal('foo@bar.baz'),
    }
    assert len(principals) == 1