import pytest
from api import Auth, API


@pytest.fixture(scope="session")
def auth():
    if not "authorization" in API.headers.keys():
        auth = Auth()
        status_code, response = auth.post()
        access_token = response['access_token']

        API.headers["authorization"] = f"Bearer {access_token}"
        API.refresh_token = response["refresh_token"]

        yield
        API.headers.pop("authorization")
        API.refresh_token = None


@pytest.fixture(scope="function")
def delete_content_type():
    API.headers.pop('Content-Type')
    yield
    API.headers['Content-Type'] = "application/json"
