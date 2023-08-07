import allure
import pytest

from api import *
from helpers import get_photo


@allure.feature("Авторизация")
class TestAuth:

    auth = Auth()

    @allure.story("Авторизация")
    def test_auth(self):
        with allure.step("Авторизация"):
            status_code, response = self.auth.post()
            assert status_code == 201
            assert "access_token", "refresh_token" in response.keys()

    @allure.story("Обновление токена")
    def test_refresh_token(self):
        status_code, response = self.auth.post()
        assert status_code == 201
        with allure.step("Обновление токена"):
            status_code, response = self.auth.put()
            assert status_code == 201
            assert "access_token", "refresh_token" in response.keys()


@allure.feature("Профиль")
class TestProfile:

    profile = Profile()
    photo_id = ""

    @allure.story("Создание профиля")
    def test_create_profile(self, auth):
        with allure.step("Создание профиля"):
            status_code, response = self.profile.post_profile()
            assert status_code == 201
            assert "name", "birthdate" in response.keys()

    @allure.story("Получение профиля")
    def test_get_profile(self, auth):
        with allure.step("Получение профиля"):
            status_code, response = self.profile.get_profile()
            assert status_code == 200
            assert "name", "birthdate" in response.keys()

    # @pytest.mark.parametrize("extension", ["jpg", "jpeg"])
    @allure.story("загрузка фото в профиль")
    def test_post_photo(self, auth, delete_content_type):
        with allure.step("загрузка фото"):
            photo = get_photo()
            status_code, response = self.profile.post_photo(files=photo)
            assert status_code == 202
            self.photo_id = response

    @allure.story("Обновление фото в профиле")
    def test_update_photo(self, auth, delete_content_type):
        with allure.step("Обновление фото профиля"):
            photo = get_photo()
            status_code, response = self.profile.update_photo(files=photo)
            assert status_code == 200

    # @allure.story("Обновление профиля")
    # def test_patch_profile(self, auth):
    #     with allure.step("Добавление био"):
    #         status_code, response = self.profile.patch_bio(bio="pupupu")
    #         assert status_code == 200

    @allure.story("Удаление профиля")
    def test_delete_profile(self, auth):
        with allure.step("Удаление профиля"):
            status_code, response = self.profile.delete_profile()
            assert status_code == 202


@allure.feature("Получение списка интересов")
class TestInterests:

    interests = Interests()

    @allure.story("Получение списка интересов")
    def test_get_interests(self, auth):
        with allure.step("Получение списка интересов"):
            status_code, response = self.interests.get()
            assert status_code == 200
            assert response
