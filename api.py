import requests


class API:

    init_data = "query_id=AAEZyN5YAAAAABnI3lg0nb8s&user=%7B%22id%22%3A1490995225%2C%22first_name%22%3A%22Y%22%2C%22last_name%22%3A%22K%22%2C%22username%22%3A%22Gog000e%22%2C%22language_code%22%3A%22ru%22%7D&auth_date=1688138457&hash=4bc946244d01de1012a90ef137b4c1b0d608405bce72023545f95c5ea5e2ebd3"
    site_url = "https://lovolab.ru/api"
    headers = {"Accept": "application/json",
                "Content-Type": "application/json",
                "user-agent": "abc"}
    refresh_token = None


class Auth(API):

    def __init__(self):
        super(Auth, self).__init__()
        self.url = f"{self.site_url}/auth"
        self.data = {
            "initData": self.init_data
        }

    def post(self):
        response = requests.post(self.url, headers=self.headers, json=self.data)
        self.headers["authorization"] = f"Bearer {response.json()['access_token']}"
        self.refresh_token = response.json()['refresh_token']
        return response.status_code, response.json()

    def put(self):
        params = {
            "refresh_token": self.refresh_token
        }
        response = requests.put(self.url, headers=self.headers, params=params)
        self.headers["authorization"] = f"Bearer {response.json()['access_token']}"
        self.refresh_token = response.json()['refresh_token']
        return response.status_code, response.json()


class Profile(API):

    def __init__(self, **kwargs):
        super(Profile, self).__init__()
        self.url = f"{self.site_url}/profile"
        self.data = {
            "name": kwargs.get("name", "string"),
            "birthdate": kwargs.get("birthdate", "2023-06-30"),
            "looking_gender": kwargs.get("looking_gender", 1),
            "gender": kwargs.get("gender", 1),
            "interests": kwargs.get("interests", [
                0
            ])
        }

    def get(self):
        response = requests.get(self.url, headers=self.headers)
        return response.status_code, response.json()

    def post(self):
        response = requests.post(self.url, headers=self.headers, json=self.data)
        return response.status_code, response.json()

    def delete(self):
        response = requests.delete(self.url, headers=self.headers)
        return response.status_code, response.json()

    def patch(self, photo_url: list):
        self.data["photo_url"] = photo_url
        response = requests.patch(f"{self.url}/photo", headers=self.headers)
        return response.status_code, response.json()

    def post_photos(self, files):
        headers = self.headers
        headers["Content-Type"] = "multipart/form-data"
        response = requests.post(self.url, headers=headers, files=files)
        return response.status_code, response.json()


class Interests(API):

    def __init__(self):
        super(Interests, self).__init__()
        self.url = f"{self.site_url}/common/interests"

    def get(self):
        response = requests.get(self.url, headers=self.headers)
        return response.status_code, response.json()

