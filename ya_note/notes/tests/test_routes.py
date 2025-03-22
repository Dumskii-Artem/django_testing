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
    DELETE_URL,
    REDIRECT_ADD_URL,
    REDIRECT_SUCCESS_URL,
    REDIRECT_LIST_URL,
    REDIRECT_EDIT_URL,
    REDIRECT_DELETE_URL,
    REDIRECT_DETAIL_URL
)


class TestRoutes(FixtureCase):
    def test_pages_availability(self):
        cases = (
            [HOME_URL, self.client, HTTPStatus.OK],
            [LOGIN_URL, self.client, HTTPStatus.OK],
            [LOGOUT_URL, self.client, HTTPStatus.OK],
            [SIGNUP_URL, self.client, HTTPStatus.OK],

            [LIST_URL, self.not_author_client, HTTPStatus.OK],
            [ADD_URL, self.not_author_client, HTTPStatus.OK],
            [SUCCESS_URL, self.not_author_client, HTTPStatus.OK],

            [DETAIL_URL, self.author_client, HTTPStatus.OK],
            [EDIT_URL, self.author_client, HTTPStatus.OK],
            [DELETE_URL, self.author_client, HTTPStatus.OK],

            [DETAIL_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
            [EDIT_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
            [DELETE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],

            [DETAIL_URL, self.client, HTTPStatus.FOUND],
            [EDIT_URL, self.client, HTTPStatus.FOUND],
            [DELETE_URL, self.client, HTTPStatus.FOUND],
        )
        for url, client, status in cases:
            with self.subTest(url=url, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        cases = (
            [ADD_URL, REDIRECT_ADD_URL],
            [DETAIL_URL, REDIRECT_DETAIL_URL],
            [DELETE_URL, REDIRECT_DELETE_URL],
            [EDIT_URL, REDIRECT_EDIT_URL],
            [LIST_URL, REDIRECT_LIST_URL],
            [SUCCESS_URL, REDIRECT_SUCCESS_URL]
        )
        for url, redirect_url in cases:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url
                )
