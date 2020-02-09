import pytest
import json
import requests_mock

from noclist import NOCList
from urllib3.exceptions import NewConnectionError


@pytest.yield_fixture(scope='module')
def auth_mock_success():
    with requests_mock.Mocker() as m:
        m.register_uri(method='GET',
                       url='http://localhost:8888/auth',
                       headers={
                           'Badsec-Authentication-Token': 'B29607BE4B3A4325773076AB7945BD51',
                       },
                       status_code=200)
        m.register_uri(method='GET',
                       url='http://localhost:8888/users',
                       status_code=200,
                       text='12345\n67890\n09876\n54321')
        yield m


@pytest.yield_fixture(scope='module')
def auth_mock_non_200():
    with requests_mock.Mocker() as m:
        m.register_uri(method='GET',
                       url='http://localhost:8888/auth',
                       headers={
                           'Badsec-Authentication-Token': 'B29607BE4B3A4325773076AB7945BD51',
                       },
                       status_code=500)
        m.register_uri(method='GET',
                       url='http://localhost:8888/users',
                       status_code=500,
                       text='12345\n67890\n09876\n54321')
        yield m


@pytest.yield_fixture(scope='module')
def auth_mock_connection_error():
    with requests_mock.Mocker() as m:
        m.register_uri(method='GET', url='http://localhost:8888/auth', exc=NewConnectionError)
        yield m


def test_connection_error(auth_mock_connection_error):
    with pytest.raises(SystemExit) as pytest_e:
        NOCList()
    assert pytest_e.type == SystemExit
    assert pytest_e.value.code == 1


def test_exit_on_status_code(auth_mock_non_200):
    with pytest.raises(SystemExit) as pytest_e:
        NOCList()
    assert pytest_e.type == SystemExit
    assert pytest_e.value.code == 1


def test_successful_retrieval(auth_mock_success):
    noclist = NOCList()
    assert noclist.user_list == json.dumps('12345\n67890\n09876\n54321'.split('\n'))
