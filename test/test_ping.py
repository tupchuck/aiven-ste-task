import pytest
from ping import ping
from requests.exceptions import InvalidSchema


# Just a dumb test
class TestPingRequest:
    def test_returns_data(self):
        url = 'https://google.com'
        message, key = ping(0, url)

        assert(message['id']) == 0
        assert(message['status_code']) == 200
        assert(message['page_title']) == 'Google'
        assert(key) == {"website": url}

    def test_wrong_url_request(self):
        with pytest.raises(InvalidSchema):
            ping(0, 'htsp://')
