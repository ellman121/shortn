from classes import ShortenedURL, UnknownShortcodeError
from unittest import mock, TestCase, main
from fastapi import HTTPException
from url_shortener import get_short_url


class TestURLShortner(TestCase):
    @mock.patch('url_shortener.short_url_store')
    def test_get_short_url_success(self, mock_surl_store):
        """
        Test `get_short_url` function returns correctly
        """
        mock_surl_store.get_url_and_increment_stats.return_value = ShortenedURL(
            shortcode="iExist",
            referenced_url="https://some.url"
        )

        resp = get_short_url("iExist")
        mock_surl_store.get_url_and_increment_stats.assert_called_with("iExist")
        
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://some.url")
    
    @mock.patch('url_shortener.short_url_store')
    def test_get_short_url_error(self, mock_surl_store):
        """
        Test `get_short_url` function handles unknown codes and raises HTTPException
        """
        mock_surl_store.get_url_and_increment_stats.side_effect = UnknownShortcodeError()

        with self.assertRaises(HTTPException):
            resp = get_short_url("error")
            mock_surl_store.get_url_and_increment_stats.assert_called_with("error")


if __name__ == '__main__':
    main()
