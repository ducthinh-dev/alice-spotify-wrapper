import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import requests
import base64
import webbrowser

from src.engine.utils import generate_random_string
from connector import Connector


class SpotifyEngine:
    def __init__(
        self,
        scope: str
    ) -> None:
        load_dotenv()
        self.__CLIENT_ID = os.environ.get("CLIENT_ID")
        self.__CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
        self.__REDIRECT_URI = os.environ.get("REDIRECT_URL")
        self.state = generate_random_string(16)
        self.__connector = Connector()

    def __authorize_url(
            self,
            response_type: str = "code"):
        state = generate_random_string(16)
        scope = "user-read-private user-read-email"
        authorize_url = "https://accounts.spotify.com/authorize?" + urlencode({
            "response_type": response_type,
            "client_id": self.__CLIENT_ID,
            "scope": scope,
            "redirect_uri": self.__REDIRECT_URI,
            "state": state
        })
        return authorize_url

    def __get_access_token(
            self,
            code: str
    ):
        credential = base64.b64encode(
            (self.__CLIENT_ID + ':' + self.__CLIENT_SECRET).encode()).decode()
        header = {
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + credential
        }
        body = {
            "code": code,
            "redirect_uri": self.__REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, headers=header, data=body)
        return response.json()
