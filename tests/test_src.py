from django.test import TestCase
from webapp import views
from django.urls import resolve

from src import __version__


def test_version():
    assert __version__ == '0.1.0'


class UrlsTest(TestCase):
    def test_root_resolves_to_home(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, views.home)

    def test_home_returns_successful(self):
        home = self.client.get('/')
        self.assertEquals(home.status_code, 200)
