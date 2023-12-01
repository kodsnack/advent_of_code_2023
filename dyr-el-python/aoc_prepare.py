"""Handles downloading of data for the Advent of Code challenge."""
from os import environ
from getpass import getuser, getpass
import requests


class SessionMissing(RuntimeError):
    """Exception when a session environment variable is missing"""
    def __init__(self):
        super().__init__("Session token missing from environmen (aoc_session)")


class PrepareAoc:
    """Handles the initiation if necessray for one day of aoc challenge."""
    def __init__(self, year, day):
        self._year = year
        self._day = day

    def get_session(self):
        """Get the session token."""
        if "aoc_session" in environ:
            return environ["aoc_session"]
        file_name = "aoc_session.txt"
        try:
            with open(file_name, "rt", encoding="utf8") as f:
                return f.read().strip()
        except FileNotFoundError:
            pass
        raise SessionMissing()

    def get_cookies(self):
        """Set up cookies for the request"""
        session = self.get_session()
        return {"session": session}

    @staticmethod
    def get_proxies():
        """Get the proxy settings from the environment"""
        proxies = {}
        for key in environ:
            if "proxy" in key or "PROXY" in key:
                protocol, _, _ = key.partition("_")
                proxies[protocol.lower()] = environ[key]
        return proxies

    def authenticate_proxies(self, proxies):
        """Trying to establish proxy authentication"""
        print("  Uh, oh. Proxy authentication needed!")
        username = getuser()
        password = getpass(prompt=f"Password for [{username}]:")
        new_proxies = dict()
        for key, value in proxies.items():
            new_proxies[key] = f"{key.lower()}://{username}:{password}@{value}"
        return new_proxies

    def load_content(self):
        """Loads content from a url with cookies and proxies"""
        url = f"https://adventofcode.com/{self._year}/day/{self._day}/input"
        cookies = self.get_cookies()
        proxies = self.get_proxies()
        print(f"Reading [{url}]")
        for key, value in proxies.items():
            print(f"  with proxy: [{key}: {value}]")
        content = ""
        while content == "":
            r = requests.get(url, cookies=cookies, proxies=proxies)
            if r.status_code == 200:
                content = r.text
                print(f"  {len(content)} characters read.")
            elif r.status_code == 407:
                proxies = self.authenticate_proxies(proxies=proxies)
            else:
                r.raise_for_status()
        return content

    def get_content(self):
        """Does all content fetch but with a cache so it will not order
        fetch if available"""
        try:
            with open(f"d{self._year}_{self._day}.txt",
                      "rt", encoding="utf8") as f:
                content = f.read()
                if len(content) > 0:
                    return content
        except FileNotFoundError:
            pass
        content = self.load_content()
        with open(f"d{self._year}_{self._day}.txt",
                  "wt", encoding="utf8") as f:
            f.write(content)
        return content
