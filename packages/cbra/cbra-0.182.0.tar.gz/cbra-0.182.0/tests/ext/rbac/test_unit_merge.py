# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.rbac.types import AccessPolicy
from cbra.ext.rbac.types import PredefinedRoleBinding


def test_duplicates_get_merged_on_binding():
    b1 = PredefinedRoleBinding.parse_obj({
        'role': 'owner',
        'members': [
            'user:foo@bar.baz',
            'user:foo@bar.baz',
        ]
    })
    members = [str(x) for x in b1.members]
    assert len(members) == 1
    assert 'user:foo@bar.baz' in members


def test_duplicates_get_merged_on_policy():
    p1 = AccessPolicy.parse_obj({
        'bindings': [
            {'role': 'foo', 'members': ['user:foo@bar.baz']},
            {'role': 'foo', 'members': ['user:bar@bar.baz']},
            {'role': 'bar', 'members': ['user:bar@bar.baz']},
        ]
    })
    assert len(p1.bindings) == 2
    members = [str(x) for x in p1.bindings[0].members]
    assert 'user:foo@bar.baz' in members
    assert 'user:bar@bar.baz' in members


def test_merge_disjoint():
    p1 = AccessPolicy.parse_obj({
        'bindings': [
            {'role': 'foo', 'members': ['user:foo@bar.baz']}
        ]
    })
    p2 = AccessPolicy.parse_obj({
        'bindings': [
            {'role': 'bar', 'members': ['user:foo@bar.baz']}
        ]
    })
    policy = p1 | p2
    assert policy.has('foo')
    assert policy.has('bar')