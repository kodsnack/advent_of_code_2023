"""Testing the advent of code prep class."""
import pytest
import aoc_prepare


@pytest.fixture(name="day_2015_04")
def create_2015_4():
    """Create some general aoc day"""
    yield aoc_prepare.PrepareAoc(2015, 4)


@pytest.fixture(name="env_session_abc123")
def set_env_abc123(monkeypatch):
    """Set the aoc session env"""
    monkeypatch.setenv("aoc_session", "abc123")
    yield


@pytest.fixture(name="env_proxy_dummies")
def set_env_dummy_http_proxy(monkeypatch):
    """Set the http proxy environment variable"""
    monkeypatch.setenv("http_proxy", "http://proxydummy.dummy.org:8080")
    monkeypatch.setenv("https_proxy", "http://proxydummy.dummy.org:8080")
    monkeypatch.setenv("HTTP_PROXY", "http://proxydummy.dummy.org:8080")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxydummy.dummy.org:8080")
    yield


@pytest.fixture(name="noenv_proxy")
def set_env_no_proxy(monkeypatch):
    """Set the http proxy environment variable"""
    monkeypatch.delenv("http_proxy", raising=False)
    monkeypatch.delenv("https_proxy", raising=False)
    monkeypatch.delenv("HTTP_PROXY", raising=False)
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    yield


def test_load_session_from_env(day_2015_04, env_session_abc123):
    """Happyily load session from environment variable"""
    assert day_2015_04.get_session() == "abc123"


def test_load_session_from_file(day_2015_04, tmp_path, monkeypatch):
    """Happily load session from file, when no environment variable is
    available"""
    path = tmp_path.absolute()
    monkeypatch.chdir(path=path)
    with open("aoc_session.txt", "tw", encoding="utf8") as f:
        f.write("def456")
    assert day_2015_04.get_session() == "def456"


def test_fail_to_load_session(day_2015_04, tmp_path, monkeypatch):
    """If neither session environment or file is available"""
    path = tmp_path.absolute()
    monkeypatch.chdir(path=path)
    with pytest.raises(aoc_prepare.SessionMissing):
        day_2015_04.get_session()


def test_happily_get_cookies(day_2015_04, env_session_abc123):
    """Check that the cookies are set up with the environmen var"""
    assert day_2015_04.get_cookies() == {"session": "abc123"}


def test_happily_get_proxies(day_2015_04, env_proxy_dummies):
    """Get the proxy setup from simulated environment, lower case http"""
    assert day_2015_04.get_proxies() == {
      "http": "http://proxydummy.dummy.org:8080",
      "https": "http://proxydummy.dummy.org:8080"
    }


def test_unable_to_find_proxy_env(day_2015_04, noenv_proxy):
    """Test get proxy with no proxy set"""
    assert day_2015_04.get_proxies() == dict()


class MonkeyResponse:
    """Class representing a response from request"""
    def __init__(self, status_code=200, text="a reply"):
        self._status_code = status_code
        self._text = text

    @property
    def status_code(self):
        """Thes status code, e.g. 200 or 404"""
        return self._status_code

    @property
    def text(self):
        """The text content of the response"""
        return self._text


def test_happily_read_from_url(day_2015_04, monkeypatch,
                               env_proxy_dummies,
                               env_session_abc123):
    """Test to read from actual url"""
    passed_args = dict()

    def monkey_request(url, proxies, cookies):
        passed_args['url'] = url
        passed_args['proxies'] = proxies
        passed_args['cookies'] = cookies
        return MonkeyResponse()

    monkeypatch.setattr(aoc_prepare.requests, "get", monkey_request)
    content = day_2015_04.load_content()
    assert passed_args['url'] == "https://adventofcode.com/2015/day/4/input"
    assert passed_args['proxies'] == {
      "https": "http://proxydummy.dummy.org:8080",
      "http": "http://proxydummy.dummy.org:8080"
    }
    assert passed_args['cookies'] == {
      "session": "abc123",
    }
    assert content == "a reply"


def test_get_from_net_if_not_cached(day_2015_04, monkeypatch,
                                    tmp_path, env_session_abc123):
    """Test to read from actual url"""
    path = tmp_path.absolute()
    monkeypatch.chdir(path=path)

    passed_args = dict()

    def monkey_request(url, proxies, cookies):
        passed_args['url'] = url
        passed_args['proxies'] = proxies
        passed_args['cookies'] = cookies
        return MonkeyResponse()

    monkeypatch.setattr(aoc_prepare.requests, "get", monkey_request)

    content = day_2015_04.get_content()
    assert content == "a reply"
    with open('d2015_4.txt', "rt", encoding="utf8") as f:
        assert f.read().strip() == "a reply"
