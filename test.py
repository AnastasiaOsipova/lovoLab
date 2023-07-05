import allure
import pytest

import helpers
from api import *
from helpers import *


@allure.feature("Авторизация")
class TestAuth:

    auth = Auth()
    @allure.story("Авторизация")
    def test_auth(self):
        with allure.step("Авторизация"):
            status_code, response = self.auth.post()
            assert status_code == 200
            assert "access_token", "refresh_token" in response.keys()

    @allure.story("Обновление токена")
    def test_refresh_token(self):
        with allure.step("Обновление токена"):
            status_code, response = self.auth.put()
            assert status_code == 200
            assert "access_token", "refresh_token" in response.keys()


@allure.feature("Профиль")
class TestProfile:

    auth = Auth()
    profile = Profile()

    @allure.story("Создание профиля")
    def test_create_profile(self):
        with allure.step("Авторизация"):
            status_code, response = self.auth.post()
            assert status_code == 200
            assert "access_token", "refresh_token" in response.keys()
        with allure.step("Создание профиля"):
            status_code, response = self.profile.post()
            assert status_code == 201
            assert "name", "birthdate" in response.keys()

    @allure.story("Получение профиля")
    def test_get_profile(self):
        # # auth
        # status_code, response = self.auth.post()
        # assert status_code == 200
        with allure.step("Получение профиля"):
            status_code, response = self.profile.get()
            assert status_code == 200
            assert "name", "birthdate" in response.keys() # , "looking_gender", "gender", "interests"

    # @allure.story("загрузка фото в профиль")
    # def test_update_photo(self):
    #     with allure.step("Авторизация"):
    #         status_code, response = self.auth.post()
    #         assert status_code == 200
    #     with allure.step("загрузка фото"):
    #         files = helpers.get_photo()
    #         status_code, response = self.profile.post_photos(files=files)
    #         assert status_code == 201

    # @allure.story("Обновление профиля")
    # def test_patch_profile(self):

    @allure.story("Удаление профиля")
    def test_delete_profile(self):
        # status_code, response = self.auth.post()
        # assert status_code == 200
        # assert "access_token", "refresh_token" in response.keys()
        with allure.step("Удаление профиля"):
            status_code, response = self.profile.delete()
            assert status_code == 200


@allure.feature("Получение списка интересов")
class TestInterests:

    auth = Auth()
    interests = Interests()

    @allure.story("Получение списка интересов")
    def test_get_interests(self):
        with allure.step("Авторизация"):
            status_code, response = self.auth.post()
            assert status_code == 200
            assert "access_token", "refresh_token" in response.keys()
        with allure.step("Получение списка интересов"):
            status_code, response = self.interests.get()
            assert status_code == 200
            assert response
