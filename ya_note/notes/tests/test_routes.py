# notes/tests/test_routes.py
from http import HTTPStatus

from notes.tests.testing_utils import (
    FixtureCase,

    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    LIST_URL,
    ADD_URL,
    SUCCESS_URL,
    DETAIL_URL,
    EDIT_URL,
    DELETE_URL
)


class TestRoutes(FixtureCase):

    def test_pages_availability(self):
        urls = (HOME_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (LIST_URL, ADD_URL, SUCCESS_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author(self):
        urls = (DETAIL_URL, EDIT_URL, DELETE_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_not_author(self):
        urls = (DETAIL_URL, EDIT_URL, DELETE_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous_client(self):
        urls = (
            DETAIL_URL,
            EDIT_URL,
            DELETE_URL,
            ADD_URL,
            SUCCESS_URL,
            LIST_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
