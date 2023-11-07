import httpx
import sys
import os


class ZaveItLogin:
    def __init__(self):
        self.username: str = "None"
        self.password: str = "None"
        self.accessToken: str = "None"
        self.refreshToken: str = "None"

        self.session = httpx.Client()

    def login(self, username, password):
        self.password = password
        self.username = username
        d = {"grantType": "password", "username": self.username, "password": self.password}
        r = self.session.post("https://api.zave.it/account/v1/pub/auth/zaver/token", json=d).json()
        print(r)
        try:
            self.accessToken = r["accessToken"]
            self.refreshToken = r["refreshToken"]
            return self.accessToken, self.refreshToken
        except:
            return False

    def get_headers(self, r=None):
        if r == "creator":
            return {
                'Host': 'api.zave.it',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://app.zave.it',
                "Authorization": "Bearer " + self.accessToken,
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://app.zave.it/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'TE': 'trailers'
            }
        return {
            'Host': 'api.zave.it',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'multipart/form-data; boundary=---------------------------212244830724033812943891773564',
            "Authorization": "Bearer " + self.accessToken,
            'Origin': 'https://app.zave.it',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://app.zave.it/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }

    def set_profile(self, image_path):
        filename = os.path.basename(image_path)
        self.session.options("https://api.zave.it/zaver/v1/me/profile-picture")
        r = self.session.put("https://api.zave.it/zaver/v1/me/profile-picture", headers=self.get_headers(), files={'image': (filename, open(image_path, 'rb'), 'image/png')})
        return r.text

    def update_token(self):
        d = {"grantType": "refreshToken", "refreshToken": self.refreshToken}
        r = self.session.post("https://api.zave.it/account/v1/pub/auth/zaver/token", json=d).json()
        print(r)
        try:
            self.accessToken = r["accessToken"]
            self.refreshToken = r["refreshToken"]
            return self.accessToken, self.refreshToken
        except:
            return False

    def change_creator(self, creator_id):
        self.session.put("https://api.zave.it/zaver/v1/me/update-creator", headers=self.get_headers("creator"), json={"id": creator_id}).json()
        return True



if __name__ == "__main__":
    z = ZaveItLogin()
    z.login("email", "password")
    z.change_creator("bw-online-shop ")
    z.set_profile(r"your/file/path")
