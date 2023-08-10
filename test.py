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
    def test_refresh_token(self, auth):
        with allure.step("Обновление токена"):
            status_code, response = self.auth.put()
            assert status_code == 201
            assert "access_token", "refresh_token" in response.keys()

    @pytest.mark.parametrize('init_data', [123, None, 1.234, (1,2,3), {"d":"kfbnfkvkfnbl"}])
    @allure.story("Негативная авторизация")
    def test_negative_auth_with_int_init_data(self, init_data):
        with allure.step("Негативная авторизация с целочисленной init_data"):
            status_code, response = self.auth.post(init_data=init_data)
            assert status_code == 422
            assert response['detail'][0]['msg'] == 'Input should be a valid string'

    @pytest.mark.parametrize('refresh_token', [123, None, 1.234, (1,2,3), {"d":"kfbnfkvkfnbl"}])
    @allure.story('Обновление невалидного токена')
    def test_negative_refresh_token(self, auth, refresh_token):
        with allure.step("Обновление невалидного токена"):
            status_code, response = self.auth.put(refresh_token=refresh_token)
            assert status_code == 422
            assert response['detail'][0]['msg'] == 'Input should be a valid string'


@allure.feature("Профиль")
class TestProfile:

    profile = Profile()
    photos_ids = []

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

    @pytest.mark.parametrize("extension", ["jpg", "jpeg"])
    @allure.story("загрузка фото в профиль")
    def test_post_photo(self, auth, delete_content_type, extension):
        with allure.step("загрузка фото"):
            photo = get_photo(extension=extension)
            status_code, response = self.profile.post_photo(files=photo)
            assert status_code == 201
            self.photos_ids.append(response['id'])

    @allure.story("Удаление фото из профиля")
    def test_delete_photo(self):
        with allure.step('Удаление фото из профиля'):
            status_code = self.profile.delete_photo(self.photos_ids[0])
            assert status_code == 204

    @pytest.mark.parametrize("extension", ["png", "svg", 'webp'])
    @allure.story("загрузка фото невалидного формата в профиль")
    def test_post_invalid_photo(self, auth, delete_content_type, extension):
        with allure.step("загрузка фото невалидного формата"):
            photo = get_photo(extension=extension)
            status_code, response = self.profile.post_photo(files=photo)
            assert status_code == 400

    @allure.story("Обновление профиля")
    def test_patch_profile(self, auth):
        with allure.step("Добавление био"):
            status_code, response = self.profile.patch_bio(bio="pupupu")
            assert status_code == 200

    @allure.story("Удаление профиля")
    def test_delete_profile(self, auth):
        with allure.step("Удаление профиля"):
            status_code, response = self.profile.delete_profile()
            assert status_code == 204


    # @allure.story("Создание профиля без авторизации")
    # def test_create_profile(self):
    #     with allure.step("Создание профиля"):
    #         status_code, response = self.profile.post_profile()
    #         assert status_code == 401
    #         assert "name", "birthdate" in response.keys()
    #
    # @allure.story("Получение профиля")
    # def test_get_profile(self, auth):
    #     with allure.step("Получение профиля"):
    #         status_code, response = self.profile.get_profile()
    #         assert status_code == 200
    #         assert "name", "birthdate" in response.keys()
    #
    # # @pytest.mark.parametrize("extension", ["jpg", "jpeg"])
    # @allure.story("загрузка фото в профиль")
    # def test_post_photo(self, auth, delete_content_type):
    #     with allure.step("загрузка фото"):
    #         photo = get_photo()
    #         status_code, response = self.profile.post_photo(files=photo)
    #         assert status_code == 201
    #         self.photo_id = response
    #
    # @allure.story("Обновление профиля")
    # def test_patch_profile(self, auth):
    #     with allure.step("Добавление био"):
    #         status_code, response = self.profile.patch_bio(bio="pupupu")
    #         assert status_code == 200
    #
    # @allure.story("Удаление профиля")
    # def test_delete_profile(self, auth):
    #     with allure.step("Удаление профиля"):
    #         status_code, response = self.profile.delete_profile()
    #         assert status_code == 204




@allure.feature("Получение списка интересов")
class TestInterests:

    interests = Interests()

    @allure.story("Получение списка интересов")
    def test_get_interests(self, auth):
        with allure.step("Получение списка интересов"):
            status_code, response = self.interests.get()
            assert status_code == 200
            assert response

    # @allure.story("Получение списка интересов без авторизации")
    # def test_get_interests_withno_auth(self):
    #     with allure.step("Получение списка интересов без авторизации"):
    #         status_code, response = self.interests.get()
    #         assert status_code == 403
