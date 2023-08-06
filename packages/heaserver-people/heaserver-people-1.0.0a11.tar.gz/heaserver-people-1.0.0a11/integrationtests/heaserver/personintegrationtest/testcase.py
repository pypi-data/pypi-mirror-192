"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.person import service
from heaserver.service.testcase.dockermongo import RealRegistryContainerConfig, DockerMongoManager
from heaserver.person.keycloakmongo import KeycloakMongoManagerForPyTest, KEYCLOAK_QUERY_ADMIN_SECRET
from heaobject.user import NONE_USER, ALL_USERS
from heaobject.registry import Property
from heaobject.person import Person
from heaserver.service.testcase.expectedvalues import Action
from heaserver.service.testcase.collection import CollectionKey
from pathlib import Path
from copy import deepcopy
from heaserver.service.testcase.collection import query_fixture_collection

db_store = {
    CollectionKey(name='properties', db_manager_cls=DockerMongoManager): [{
        'id': '666f6f2d6261722d71757578',
        'name': KEYCLOAK_QUERY_ADMIN_SECRET,
        'value': None,
        'owner': NONE_USER,
        'type': Property.get_type_name()
    }],
    CollectionKey(name=service.MONGODB_PERSON_COLLECTION, db_manager_cls=DockerMongoManager): [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus Max',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [{
            'invite': None,
            'permissions': ['VIEWER'],
            'type': 'heaobject.root.ShareImpl',
            'user': ALL_USERS
        }],
        'source': None,
        'first_name': 'Reximus',
        'last_name': 'Max',
        'type': Person.get_type_name(),
        'version': None,
        'phone_number': None,
        'preferred_name': None,
        'email': 'reximus.max@example.com',
        'id_labs_collaborator': None,
        'id_labs_manage': None,
        'id_labs_member': None,
        'id_projects_collaborator': None,
        'title': None
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Luximus Max',
            'invites': [],
            'modified': None,
            'name': 'luximus',
            'owner': NONE_USER,
            'shares': [{
                'invite': None,
                'permissions': ['VIEWER'],
                'type': 'heaobject.root.ShareImpl',
                'user': ALL_USERS
            }],
            'source': None,
            'first_name': 'Luximus',
            'last_name': 'Max',
            'type': Person.get_type_name(),
            'version': None,
            'phone_number': None,
            'preferred_name': None,
            'email': 'luximus.max@example.com',
            'id_labs_collaborator': None,
            'id_labs_manage': None,
            'id_labs_member': None,
            'id_projects_collaborator': None,
            'title': None
        }]}

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a32'

db_store_ = deepcopy(db_store)
secret = Path('.secret').read_text().strip()
prop = next((org for org in query_fixture_collection(db_store_, 'properties', strict=False) or [] if
             org['id'] == '666f6f2d6261722d71757578'), None)
prop['value'] = secret

TestCase = get_test_case_cls_default(coll=service.MONGODB_PERSON_COLLECTION,
                                     href='http://localhost:8080/people/',
                                     wstl_package=service.__package__,
                                     db_manager_cls=KeycloakMongoManagerForPyTest,
                                     fixtures=db_store_,
                                     get_actions=[Action(name='heaserver-people-person-get-properties',
                                                         rel=['hea-properties']),
                                                  Action(name='heaserver-people-person-get-self',
                                                         url='http://localhost:8080/people/{id}',
                                                         rel=['self'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-people-person-get-properties',
                                                             rel=['hea-properties']),
                                                      Action(name='heaserver-people-person-get-self',
                                                             url='http://localhost:8080/people/{id}',
                                                             rel=['self'])
                                                      ],
                                     registry_docker_image=RealRegistryContainerConfig(HEASERVER_REGISTRY_IMAGE),
                                     duplicate_action_name='heaserver-people-person-duplicate-form',
                                     exclude=['body_put', 'body_post'])
