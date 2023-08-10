import pytest
from api import Auth, API, Profile


@pytest.fixture(scope="class")
def auth(request):
    if not "authorization" in API.headers.keys():
        auth = Auth()
        status_code, response = auth.post()
        access_token = response['access_token']

        API.headers["authorization"] = f"Bearer {access_token}"
        API.refresh_token = response["refresh_token"]

        # Определение функции финализатора
        def finalize():
            API.headers.pop("authorization")
            API.refresh_token = None

        # Добавление финализатора с помощью addfinalizer()
        request.addfinalizer(finalize)

        # Возвращается значение True для успешной инициализации auth
        return True

@pytest.fixture(scope="function")
def delete_content_type():
    API.headers.pop('Content-Type')
    yield
    API.headers['Content-Type'] = "application/json"

@pytest.fixture()
def delete_photo(photos_ids):
    profile = Profile()
    for photo_id in photos_ids:
        status_code = profile.delete_photo(photo_id)
        assert status_code == 204

