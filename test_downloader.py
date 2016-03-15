from unittest import TestCase
from mock import MagicMock

from spider import Downloader
from spider import Queue


class TestDownloader(TestCase):

    def test_download_not_resolve(self):
        queue = Queue()
        queue.push = MagicMock()

        downloader = Downloader(queue)
        downloader.download('http://notresolve.site/')
        queue.push.assert_not_called()

    def test_download_404(self):
        queue = Queue()
        queue.push = MagicMock()
        downloader = Downloader(queue)
        downloader.download('http://www.google.com/_filenotexisting')
        queue.push.assert_not_called()

    def test_extract_simple(self):
        sample = '''
        <!DOCTYPE html>
        <html>
        <body>
            <a href="http://www.w3schools.com">This is a link</a>

        </body>
        </html>
        '''
        downloader = Downloader(None)
        self.assertListEqual(list(downloader._extract(sample)), [u'http://www.w3schools.com'])

    def test_extract_images(self):
        sample = '''
        <!DOCTYPE html><html>
        <body>
            <h2>Spectacular Mountain</h2>
            <img src="pic_mountain.jpg" alt="Mountain View" style="width:304px;height:228px;">
        </body>
        </html>
        '''
        downloader = Downloader(None)
        self.assertListEqual(list(downloader._extract(sample)), [u'pic_mountain.jpg'])

    def test_extract_links(self):
        sample = '''
        <html><head>
            <link rel="icon" href="/favicon.ico" type="image/x-icon">
            <link rel="stylesheet" href="/lib/w3.css">
            </head>
        <body></body><html>
        '''
        downloader = Downloader(None)
        self.assertListEqual(list(downloader._extract(sample)), [u'/favicon.ico', u'/lib/w3.css'])

    def test_normalize_url(self):
        downloader = Downloader(None)
        self.assertEqual(downloader._normalize('http://www.test.com', 'http://test2.com'), 'http://test2.com')

    def test_test_normalize_absolute(self):
        downloader = Downloader(None)
        self.assertEqual(downloader._normalize('http://www.test.com/norelevant', '/test'), 'http://www.test.com/test')

    def test_normalize_relative(self):
        downloader = Downloader(None)
        self.assertEqual(downloader._normalize('http://www.test.com/dir/resources.html', 'image.gif'), 'http://www.test.com/dir/image.gif')