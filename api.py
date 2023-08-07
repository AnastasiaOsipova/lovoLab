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
        self.url = f"{self.site_url}/v1/auth"
        self.data = {
            "initData": self.init_data
        }

    def post(self):
        response = requests.post(self.url, headers=self.headers, json=self.data)
        self.headers["authorization"] = f"Bearer {response.json()['access_token']}"
        self.refresh_token = response.json()['refresh_token']
        return response.status_code, response.json()

    def put(self):
        body = {
            "refresh_token": self.refresh_token
        }
        response = requests.put(self.url, headers=self.headers, json=body)
        self.headers["authorization"] = f"Bearer {response.json()['access_token']}"
        self.refresh_token = response.json()['refresh_token']
        return response.status_code, response.json()


class Profile(API):

    def __init__(self, **kwargs):
        super(Profile, self).__init__()
        self.url = f"{self.site_url}/v1/profile"
        self.data = {
            "name": kwargs.get("name", "string"),
            "birthdate": kwargs.get("birthdate", "2000-06-30"),
            "looking_gender": kwargs.get("looking_gender", 1),
            "gender": kwargs.get("gender", 1),
            "interests": kwargs.get("interests", [
                0
            ])
        }

    def get_profile(self):
        response = requests.get(self.url, headers=self.headers)
        return response.status_code, response.json()

    def post_profile(self):
        response = requests.post(self.url, headers=self.headers, json=self.data)
        return response.status_code, response.json()

    def delete_profile(self):
        response = requests.delete(self.url, headers=self.headers)
        return response.status_code, response.json()

    def patch_bio(self, bio=""):
        data = {
            "bio": bio
        }
        response = requests.patch(self.url, headers=self.headers, json=data)
        return response.status_code, response.json()

    def post_photo(self, files):
        response = requests.post(f"{self.url}/photo", headers=self.headers, files=files)
        return response.status_code, response.json()

    def update_photo(self, files):
        response = requests.patch(f"{self.url}/photo", headers=self.headers, files=files)
        return response.status_code, response.json()

    def add_interests(self, files):
        response = requests.put(f"{self.url}/interests", headers=self.headers, files=files)
        return response.status_code, response.json()

    def delete_photo(self, photo_id):
        response = requests.delete(f"{self.url}/photo/{photo_id}", headers=self.headers)
        return response.status_code, response.json()


class Interests(API):

    def __init__(self):
        super(Interests, self).__init__()
        self.url = f"{self.site_url}/v1/interests"

    def get(self):
        response = requests.get(self.url, headers=self.headers)
        return response.status_code, response.json()
