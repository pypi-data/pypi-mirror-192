from requests import get, post
from replit_bot import post as gql
import requests
import random


class usersErrors:
    class InvalidParam(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

        pass

    class UnknownError(Exception):
        def __init__(self, message="An unidentified error has occurred!"):
            self.message = message
            super().__init__(self.message)

        pass

    class BadRequest(Exception):
        def __init__(self, message="Something went terribly wrong."):
            self.message = message
            super().__init__(self.message)

        pass


class Client:
    def __init__(this, proxies: str, timeout: int):
        this.author = "beliefs"
        this.proxies = proxies
        this.timeout = timeout
        this.session = requests.Session()

    def clear():
        print("\033c", end="", flush=True)

    def Replit(this, username: str, api=None):
        """
        :params username, api: given username to check, whether or not to check using api or standard URL.
        :usage: The username is checked on Replit using their api & base URL.
        """
        if api in (None, False):
            base = this.session.get(
                "https://replit.com/@%s" % username,
                proxies=this.proxies,
                timeout=this.timeout,
            )
            if base.status_code == 404:
                return "%s available." % username
            elif base.status_code == 200:
                return "%s taken." % username
        elif api == True:
            base = gql("", "userByUsername", {"username": username})["userByUsername"]
            Client.clear()
            if base != None:
                return "%s taken." % username
            else:
                return "%s available." % username
        raise usersErrors.InvalidParam(
            "Invalid Api Param; correct usage False or True."
        )

    def Twitch(this, username: str):
        """
        :params username: given username to check.
        :usage: The username is checked on Twitch using their gql API.
        """
        base = this.session.post(
            "https://gql.twitch.tv/gql",
            headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
            json=[
                {
                    "operationName": "UsernameValidator_User",
                    "variables": {"username": username},
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "fd1085cf8350e309b725cf8ca91cd90cac03909a3edeeedbd0872ac912f3d660",
                        }
                    },
                }
            ],
            proxies=this.proxies,
            timeout=this.timeout,
        ).json()[0]["data"]["isUsernameAvailable"]
        if base != True:
            return "%s taken." % username
        else:
            return "%s available." % username

    def Twitter(this, username: str):
        """
        :params username: given username to check
        :usage: checks username via api
        """
        base = this.session.get(
            "https://api.twitter.com/i/users/username_available.json?username=%s"
            % username,
            proxies=this.proxies,
            timeout=this.timeout,
        ).json()["valid"]
        if base == True:
            return "%s available." % username
        else:
            return "%s taken." % username

    def Instagram(this, username: str):
        """
        :params username: username being checked
        :usage: checks username via api
        """
        base = this.session.post(
            "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            headers={"X-CSRFToken": "en"},
            data={
                "email": "",
                "username": username,
                "first_name": "",
                "opt_into_one_tap": "false",
            },
            proxies=this.proxies,
            timeout=this.timeout,
        )
        if '"username": [{"message": ' in base.text:
            return "%s taken." % username
        elif "spam" in base.text:
            return "rate restriction."
        else:
            return "%s available." % username

    def Github(this, username: str, api=None):
        """
        :params username, api: username being checked, which mode to be used to check.
        """
        if api == None:
            base = this.session.get(
                "https://github.com/%s" % username,
                proxies=this.proxies,
                timeout=this.timeout,
            ).status_code
            if base == 404:
                return "%s available." % username
            elif base == 200:
                return "%s taken." % username
        return "not finished yet."
