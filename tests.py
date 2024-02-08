import datetime
from classes import DuplicateShortcodeError, ShortenedURL, URLStats, UnknownShortcodeError
from unittest import mock, TestCase, main
from fastapi import HTTPException

from url_shortener import CreateRequestBody, create_short_url, get_short_url, get_stats


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
            get_short_url("error")
            mock_surl_store.get_url_and_increment_stats.assert_called_with("error")

    @mock.patch('url_shortener.short_url_store')
    def test_get_stats_success(self, mock_surl_store):
        """
        Test `get_stats` function returns correctly
        """
        mock_surl_store.get_url_stats.return_value = URLStats(
            lastRedirect=datetime.datetime.now(),
            created=datetime.datetime.now(),
            redirectCount=5
        )

        resp = get_stats("iExist")
        mock_surl_store.get_url_stats.assert_called_with("iExist")
        self.assertEqual(resp.redirectCount, 5)
        self.assertIsNotNone(resp.lastRedirect)
        self.assertIsNotNone(resp.created)
    
    @mock.patch('url_shortener.short_url_store')
    def test_get_stats_error(self, mock_surl_store):
        """
        Test `get_stats` function handles unknown codes and raises HTTPException
        """
        mock_surl_store.get_url_stats.side_effect = UnknownShortcodeError()

        with self.assertRaises(HTTPException):
            get_stats("error")
            mock_surl_store.get_url_stats.assert_called_with("error")
    

    @mock.patch('url_shortener.short_url_store')
    def test_create_short_url_success(self, mock_surl_store):
        """
        Test `create_short_url` function returns correctly
        """
        new_shortcode = "123456"
        new_ref_url = "https://some.url"
        new_shortened_url = ShortenedURL(
            shortcode=new_shortcode,
            referenced_url=new_ref_url
        )
        
        mock_surl_store.add_url_to_store.return_value = new_shortened_url
        resp = create_short_url(CreateRequestBody(
            url=new_ref_url,
            shortcode=new_shortcode
        ))
        mock_surl_store.add_url_to_store.assert_called_with(new_shortened_url)
        
        self.assertEqual(resp, { "shortcode": new_shortcode })

    @mock.patch('url_shortener.short_url_store')
    def test_create_short_url_errors(self, mock_surl_store):
        """
        Test `create_short_url` returns correct error codes with invalid input
        """
        # No body case => 400
        with self.assertRaises(HTTPException) as e:
            create_short_url(None)
        self.assertEqual(e.exception.status_code, 400)

        # No URL case => 400
        with self.assertRaises(HTTPException) as e:
            create_short_url(CreateRequestBody(
                shortcode="123456",
                url=None
            ))
        self.assertEqual(e.exception.status_code, 400)

        # Invlaid URL case => 400
        with self.assertRaises(HTTPException) as e:
            create_short_url(CreateRequestBody(
                shortcode="123456",
                url="bobbadurl"
            ))
        self.assertEqual(e.exception.status_code, 400)

        # Invalid shortcode case => 412
        with self.assertRaises(HTTPException) as e:
            create_short_url(CreateRequestBody(
                shortcode="12",
                url="https://goodurl.com"
            ))
        self.assertEqual(e.exception.status_code, 412)

        # Duplicate shortcode case => 409
        with self.assertRaises(HTTPException) as e:
            mock_surl_store.add_url_to_store.side_effect = DuplicateShortcodeError()
            create_short_url(CreateRequestBody(
                shortcode="123456",
                url="https://goodurl.com"
            ))
        self.assertEqual(e.exception.status_code, 409)
        

if __name__ == '__main__':
    main()
