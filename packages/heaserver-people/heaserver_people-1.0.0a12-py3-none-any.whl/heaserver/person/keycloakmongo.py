import configparser
from typing import Generator, Any
from contextlib import contextmanager, ExitStack
from heaserver.service.db.mongo import MongoManager, Mongo
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaserver.service.testcase.mockmongo import MockMongoManager, MockMongo
from heaserver.service.testcase.testenv import DockerContainerConfig, DockerVolumeMapping
from heaserver.service.testcase.docker import start_other_container
from heaserver.service import appproperty
from heaserver.service.client import get_property
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.heaobjectsupport import PermissionGroup
from heaserver.service.util import retry
from heaobject.person import Person
from heaobject.user import NONE_USER, ALL_USERS
from heaobject.root import ShareImpl, Permission, Share
from aiohttp.web import Request
from yarl import URL
import logging
from pathlib import Path
from datetime import datetime
from docker.errors import APIError
import os
import requests


KEYCLOAK_QUERY_ADMIN_SECRET = 'KEYCLOAK_QUERY_ADMIN_SECRET'
DEFAULT_CLIENT_ID = 'client-cli'
DEFAULT_REALM = 'hea'
DEFAULT_HOST = 'https://localhost:8444'
DEFAULT_SECRET_FILE = '.secret'
CONFIG_SECTION = 'Keycloak'
KEYCLOAK_IMAGE = 'jboss/keycloak:15.0.2'


class KeycloakMongo(Mongo):
    def __init__(self, config: configparser.ConfigParser | None = None,
                 access_token: str | None = None,
                 client_id: str | None = DEFAULT_CLIENT_ID,
                 realm: str | None = DEFAULT_REALM,
                 host: str | None = DEFAULT_HOST,
                 secret: str | None = None,
                 secret_file: str | None = DEFAULT_SECRET_FILE,
                 verify_ssl: bool = True):
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
        """
        Request an access token from Keycloak.

        :param request: the HTTP request (request).
        :return: the access token or None if not found.
        """
        session = request.app[appproperty.HEA_CLIENT_SESSION]
        logger = logging.getLogger(__name__)

        token_url = URL(self.host) / 'auth' / 'realms' / self.realm / 'protocol' / 'openid-connect' / 'token'
        logger.debug('Requesting new access token using credentials')
        secret_property = await get_property(request.app, KEYCLOAK_QUERY_ADMIN_SECRET)
        if secret_property is not None:
            secret = secret_property.value
            logger.debug('Read secret from registry service')
        elif self.secret_file and (secret_file_path := Path(self.secret_file)).exists():
            secret = secret_file_path.read_text()
            logger.debug('Read secret from file')
        elif self.secret:
            secret = self.secret
            logger.debug('Read secret from config')
        else:
            raise ValueError('No secret defined')
        token_body = {
            'client_secret': secret,
            'client_id': 'admin-cli',
            'grant_type': 'client_credentials'
        }
        logger.debug('Going to verify ssl? %r', self.verify_ssl)
        async with session.post(token_url, data=token_body, verify_ssl=self.verify_ssl) as response_:
            content = await response_.json()
            logging.getLogger(__name__).debug(f'content {content}')
            access_token = content['access_token']
        return access_token

    async def get_users(self, request: Request, access_token: str, params: dict[str, str] | None = None) -> \
        list[Person]:
        """
        Gets a list of users from Keycloak using the '/auth/admin/realms/{realm}/users' REST API call.

        :param access_token: the access token to use (required).
        :param params: any query parameters to add to the users request.
        :return: a list of Person objects, or the empty list if there are none.
        """
        logger = logging.getLogger(__name__)
        session = request.app[appproperty.HEA_CLIENT_SESSION]
        db = request.app[appproperty.HEA_DB]
        users_url = URL(db.host) / 'auth' / 'admin' / 'realms' / db.realm / 'users'

        if params:
            params_ = {}
            for k, v in params.items():
                match k:
                    case 'name':
                        params_['username'] = v
                    case 'first_name':
                        params_['firstName'] = v
                    case 'last_name':
                        params_['lastName'] = v
                    case _:
                        params_[k] = v
            users_url_ = users_url.with_query(params_)
        else:
            users_url_ = users_url
        async with session.get(users_url_,
                               headers={'Authorization': f'Bearer {access_token}', 'cache-control': 'no-cache'},
                               verify_ssl=db.verify_ssl) as response_:
            response_.raise_for_status()
            user_json = await response_.json()
            logger.debug(f'Response was {user_json}')
            persons = []
            for user in user_json:
                person = self.__keycloak_user_to_person(user)
                if not params or all(p for p in params.keys() if getattr(person, p) == params[p]):
                    persons.append(person)
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
        session = request.app[appproperty.HEA_CLIENT_SESSION]
        db = request.app[appproperty.HEA_DB]
        user_url = URL(db.host) / 'auth' / 'admin' / 'realms' / db.realm / 'users' / id_
        async with session.get(user_url,
                               headers={'Authorization': f'Bearer {access_token}', 'cache-control': 'no-cache'},
                               verify_ssl=db.verify_ssl) as response_:
            user_json = await response_.json()
            logger.debug(f'Response was {user_json}')
            if 'error' in user_json:
                if user_json['error'] == 'User not found':
                    return None
                else:
                    raise ValueError(user_json['error'])
            return self.__keycloak_user_to_person(user_json)

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
        person.created = datetime.fromtimestamp(user['createdTimestamp'] / 1000.0)
        person.owner = NONE_USER
        share = ShareImpl()
        share.user = ALL_USERS
        share.permissions = [Permission.VIEWER]
        person.shares = [share]
        return person


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


class KeycloakMongoManager(MongoManager):
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


def _has_permission(request: Request, person: Person) -> bool:
    return request.headers[SUB] == person.owner or person.owner == ALL_USERS


def _shares_with_user(request: Request, person: Person) -> list[Share]:
    return [s for s in person.shares if s.user == request.headers[SUB] and len(
        set(PermissionGroup.GETTER_PERMS.perms).intersection(s.permissions)) > 0]


_p1 = Person()
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
_p2 = Person()
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
