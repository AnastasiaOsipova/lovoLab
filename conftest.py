import pytest
from api import Auth


@pytest.fixture(scope="session")
def auth_and_write_access_token():
    Auth().post()
    yield
    pass
