import unittest
import mock
from sqlalchemy import create_mock_engine

from url_shortener import get_short_url


db_engine = create_mock_engine("", None)

class TestURLShortner(unittest.TestCase):
    @mock.patch('url_shortener.short_url_store')
    def test_get_short_url(self, mock_surl_store):
        """
        Test that we are able to get an existing URL
        """
        conn = db_engine.connect()
        get_short_url(conn, "iExist")

        mock_surl_store.get_url_and_increment_stats.assert_called_with(conn, "iExist")


if __name__ == '__main__':
    unittest.main()
