import configparser
import logging
import os
from contextlib import ExitStack, contextmanager
from datetime import datetime
from typing import Generator, Any

import requests
from aiohttp.web_request import Request
from docker.errors import APIError
from heaobject.person import Person
from heaobject.root import ShareImpl, Permission
from heaobject.user import NONE_USER, ALL_USERS
from heaserver.service import appproperty
from heaserver.service.testcase.docker import start_other_container
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaserver.service.testcase.mockmongo import MockMongoManager, MockMongo
from heaserver.service.testcase.testenv import DockerContainerConfig, DockerVolumeMapping
from heaserver.service.util import retry
from yarl import URL

from heaserver.person.keycloakmongo import KEYCLOAK_IMAGE, DEFAULT_CLIENT_ID, DEFAULT_REALM, DEFAULT_SECRET_FILE, \
    KeycloakMongo, DEFAULT_HOST, CONFIG_SECTION, _has_permission


class KeycloakDockerMongoManager(DockerMongoManager):
    KEYCLOAK_CONTAINER_CONFIG = DockerContainerConfig(image=KEYCLOAK_IMAGE,
                                                      ports=[8080, 8443],
                                                      volumes=[
                                                          DockerVolumeMapping(host=f'{os.getcwd()}/keycloak',
                                                                              container='/tmp')
                                                      ],
                                                      check_path='/auth/',
                                                      env_vars={
                                                          'KEYCLOAK_USER': 'admin',
                                                          'KEYCLOAK_PASSWORD': 'admin',
                                                          'KEYCLOAK_IMPORT': '/tmp/hea-export.json'
                                                      })

    def __init__(self, access_token: str | None = None,
                 client_id: str | None = None,
                 realm: str | None = None,
                 secret: str | None = None,
                 secret_file: str | None = None,
                 verify_ssl: bool = True):
        super().__init__()
        self.__access_token: str | None = str(access_token) if access_token is not None else None
        self.__client_id = str(client_id) if client_id is not None else DEFAULT_CLIENT_ID
        self.__realm = str(realm) if realm is not None else DEFAULT_REALM
        self.__secret: str | None = str(secret) if secret is not None else None
        self.__secret_file: str | None = str(secret_file) if secret_file is not None else DEFAULT_SECRET_FILE
        self.__verify_ssl: bool = bool(verify_ssl)
        from testcontainers.core.container import DockerContainer
        self.__keycloak: DockerContainer | None = None
        self.__keycloak_external_url: str | None = None

    @property
    def access_token(self) -> str | None:
        return self.__access_token

    @access_token.setter
    def access_token(self, access_token: str | None):
        self.__access_token = str(access_token) if access_token is not None else None

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, client_id: str):
        self.__client_id = str(client_id) if client_id is not None else DEFAULT_CLIENT_ID

    @property
    def realm(self) -> str:
        return self.__realm

    @realm.setter
    def realm(self, realm: str):
        self.__realm = str(realm) if realm is not None else DEFAULT_REALM

    @property
    def secret(self) -> str | None:
        return self.__secret

    @secret.setter
    def secret(self, secret: str | None):
        self.__secret = str(secret) if secret is not None else None

    @property
    def secret_file(self) -> str | None:
        return self.__secret_file

    @secret_file.setter
    def secret_file(self, secret_file: str | None):
        self.__secret_file = str(secret_file) if secret_file is not None else None

    @property
    def verify_ssl(self) -> bool:
        return self.__verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, verify_ssl: bool):
        self.__verify_ssl = bool(verify_ssl)

    @property
    def keycloak_external_url(self) -> str | None:
        return self.__keycloak_external_url

    @retry(APIError)
    def start_database(self, context_manager: ExitStack):
        """
        Starts the database container, using the image defined in DockerImages.MONGODB. This must be called prior to
        calling get_config_file_section().

        :param context_manager: the context manager to which to attach this container. The container will shut down
        automatically when the context manager is closed.
        """
        self.__keycloak, self.__keycloak_external_url = start_other_container(type(self).KEYCLOAK_CONTAINER_CONFIG,
                                                                              context_manager)
        super().start_database(context_manager)

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[KeycloakMongo, None, None]:
        yield KeycloakMongo(config=config,
                            access_token=self.access_token,
                            client_id=self.client_id,
                            realm=self.realm,
                            host=self.keycloak_external_url,
                            secret=self.secret,
                            secret_file=self.secret_file,
                            verify_ssl=self.verify_ssl)


class KeycloakMongoManagerForTesting(KeycloakDockerMongoManager):
    def __init__(self):
        super().__init__()

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[KeycloakMongo, None, None]:
        logger = logging.getLogger(__name__)
        mongo = KeycloakMongoForTesting(config=config, host=self.keycloak_external_url)
        users = [{
            'username': 'reximus',
            'firstName': 'Reximus',
            'lastName': 'Max',
            'email': 'reximus.max@example.com',
            'emailVerified': True,
            'credentials': [{
                'value': 'reximus',
                'temporary': False
            }],
            'enabled': True
        },
        {
            'username': 'luximus',
            'firstName': 'Luximus',
            'lastName': 'Max',
            'email': 'luximus.max@example.com',
            'emailVerified': True,
            'credentials': [{
                'value': 'luximus',
                'temporary': False
            }],
            'enabled': True
        }]
        for user in users:
            response = requests.post(mongo.token_url, data=mongo.token_body)
            response.raise_for_status()
            logger.debug('Got token request %s', response)
            access_token = response.json()['access_token']
            response = requests.post(str(URL(mongo.host) / 'auth' / 'admin' / 'realms' / mongo.realm / 'users'),
                                     json=user, headers={'Authorization': f'Bearer {access_token}'})
            response.raise_for_status()
            logger.debug('New user %s requested, got response %s', user, response)

        yield mongo


class KeycloakMongoManagerForPyTest(KeycloakDockerMongoManager):
    def __init__(self):
        super().__init__()

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[KeycloakMongo, None, None]:
        logger = logging.getLogger(__name__)
        mongo = KeycloakMongoForPyTest(config=config, host=self.keycloak_external_url)
        response = requests.post(mongo.token_url, data=mongo.token_body)
        response.raise_for_status()
        logger.debug('Got token request %s', response)
        access_token = response.json()['access_token']
        users = [{
            'username': 'reximus',
            'firstName': 'Reximus',
            'lastName': 'Max',
            'email': 'reximus.max@example.com',
            'emailVerified': True,
            'credentials': [{
                'value': 'reximus',
                'temporary': False
            }],
            'enabled': True
        },
        {
            'username': 'luximus',
            'firstName': 'Luximus',
            'lastName': 'Max',
            'email': 'luximus.max@example.com',
            'emailVerified': True,
            'credentials': [{
                'value': 'luximus',
                'temporary': False
            }],
            'enabled': True
        }]
        for user in users:
            response = requests.post(str(URL(mongo.host) / 'auth' / 'admin' / 'realms' / mongo.realm / 'users'),
                                     json=user, headers={'Authorization': f'Bearer {access_token}'})
            response.raise_for_status()
            logger.debug('New user %s requested, got response %s', user, response)

        yield mongo


class KeycloakMockMongo(MockMongo):
    def __init__(self, config: configparser.ConfigParser | None = None,
                 access_token: str | None = None,
                 client_id: str | None = DEFAULT_CLIENT_ID,
                 realm: str | None = DEFAULT_REALM,
                 host: str | None = DEFAULT_HOST,
                 secret: str | None = None,
                 secret_file: str | None = DEFAULT_SECRET_FILE,
                 verify_ssl: bool = False):
        super().__init__(config)
        if config and CONFIG_SECTION in config:
            _section = config[CONFIG_SECTION]
            self.__realm = _section.get('Realm', realm)
            self.__verify_ssl = _section.getboolean('VerifySSL', verify_ssl)
            self.__host = _section.get('Host', host)
            self.__secret = _section.get('Secret', secret)
            self.__secret_file = _section.get('SecretFile', secret_file)
        else:
            self.__realm = realm
            self.__verify_ssl = verify_ssl
            self.__host = host
            self.__secret = secret
            self.__secret_file = secret_file

        self.__access_token = access_token
        self.__client_id = client_id

    @property
    def access_token(self) -> str | None:
        return self.__access_token

    @property
    def client_id(self) -> str:
        return self.__client_id

    @property
    def realm(self) -> str:
        return self.__realm

    @property
    def host(self) -> str:
        return self.__host

    @property
    def secret(self) -> str | None:
        return self.__secret

    @property
    def secret_file(self) -> str | None:
        return self.__secret_file

    @property
    def verify_ssl(self) -> bool:
        return self.__verify_ssl

    async def get_keycloak_access_token(self, request: Request) -> str:
        return '12345678'

    async def get_users(self, request: Request, access_token: str, params: dict[str, str] | None = None) -> list[
        Person]:
        logger = logging.getLogger(__name__)

        persons = []
        for r in (_p1, _p2):
            if params is None or all(hasattr(r, k) and v == getattr(r, k) for k, v in params.items()):
                persons.append(r)
        return persons

    async def get_user(self, request: Request, access_token: str, id_: str) -> Person | None:
        """
        Gets the user from Keycloak with the given id using the '/auth/admin/realms/{realm}/users/{id}' REST API call.

        :param access_token: the access token to use (required).
        :param session: the client session (required).
        :param id_: the user id (required).
        :return: a Person object.
        :raises ClientResponseError if an error occurred or the person was not found.
        """
        logger = logging.getLogger(__name__)
        match (request.match_info['id']):
            case '666f6f2d6261722d71757578':
                return _p1 if _has_permission(request, _p1) else None
            case '0123456789ab0123456789ab':
                return _p2 if _has_permission(request, _p2) else None
            case _:
                return None

    def __keycloak_user_to_person(self, user: dict[str, Any]) -> Person:
        """
        Converts a user JSON object from Keycloak to a HEA Person object.

        :param user: a Keycloak user object as a JSON dict.
        :return: a Person object.
        """
        person = Person()
        person.id = user['id']
        person.name = user['username']
        person.first_name = user.get('firstName')
        person.last_name = user.get('lastName')
        person.email = user.get('email')
        person.created = datetime(2022, 1, 1)
        person.owner = NONE_USER
        share = ShareImpl()
        share.user = ALL_USERS
        share.permissions = [Permission.VIEWER]
        person.shares = [share]
        return person


class KeycloakMockMongoManager(MockMongoManager):
    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[MockMongo, None, None]:
        yield KeycloakMockMongo(config)


class KeycloakMongoForTesting(KeycloakMongo):
    def __init__(self, config: configparser.ConfigParser | None = None, host: str | None = None):
        super().__init__(config=config, host=host, verify_ssl=True)

    @property
    def token_url(self) -> str:
        return str(URL(self.host) / 'auth' / 'realms' / 'master' / 'protocol' / 'openid-connect' / 'token')

    @property
    def token_body(self) -> dict[str, str]:
        return {
            'username': 'admin',
            'password': 'admin',
            'client_id': 'admin-cli',
            'grant_type': 'password'
        }

    async def get_keycloak_access_token(self, request: Request) -> str:
        """
        Request an access token from Keycloak.

        :param request: the HTTP request (required).
        :return: the access token or None if not found.
        """
        session = request.app[appproperty.HEA_CLIENT_SESSION]
        logger = logging.getLogger(__name__)
        logger.debug('Requesting new access token using credentials')

        async with session.post(self.token_url, data=self.token_body, verify_ssl=self.verify_ssl) as response_:
            content = await response_.json()
            logging.getLogger(__name__).debug(f'content {content}')
            access_token = content['access_token']
        return access_token


class KeycloakMongoForPyTest(KeycloakMongoForTesting):
    async def get_users(self, request: Request, access_token: str, params: dict[str, str] | None = None) -> \
            list[Person]:
        users = await super().get_users(request, access_token, params)
        for user in users:
            match user.name:
                case 'reximus':
                    user.id = '666f6f2d6261722d71757578'
                case 'luximus':
                    user.id = '0123456789ab0123456789ab'
            user.created = None
            user.modified = None
        return users


_p1 = Person()
_p2 = Person()
_p1.from_dict({
    'id': '666f6f2d6261722d71757578',
    'created': '2022-01-01T00:00:00',
    'derived_by': None,
    'derived_from': [],
    'description': None,
    'display_name': 'Reximus Max',
    'invites': [],
    'modified': None,
    'name': 'reximusmax',
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
    'type': 'heaobject.person.Person',
    'version': None,
    'title': None,
    'phone_number': None,
    'preferred_name': None,
    'id_labs_collaborator': None,
    'id_labs_manage': None,
    'id_labs_member': None,
    'id_projects_collaborator': None,
    'email': None
})
_p2.from_dict({
    'id': '0123456789ab0123456789ab',
    'created': '2022-01-01T00:00:00',
    'derived_by': None,
    'derived_from': [],
    'description': None,
    'display_name': 'Luximus Max',
    'invites': [],
    'modified': None,
    'name': 'luximusmax',
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
    'type': 'heaobject.person.Person',
    'version': None,
    'title': None,
    'phone_number': None,
    'preferred_name': None,
    'id_labs_collaborator': None,
    'id_labs_manage': None,
    'id_labs_member': None,
    'id_projects_collaborator': None,
    'email': None
})
