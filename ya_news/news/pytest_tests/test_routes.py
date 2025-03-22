from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


HOME_URL = pytest.lazy_fixture('home_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
EDIT_URL = pytest.lazy_fixture('edit_url')

REDIRECT_DELETE_URL = pytest.lazy_fixture('redirect_delete_url')
REDIRECT_EDIT_URL = pytest.lazy_fixture('redirect_edit_url')

CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client_fixure, status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),

        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (DETAIL_URL, CLIENT, HTTPStatus.OK),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (DELETE_URL, CLIENT, HTTPStatus.FOUND),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (EDIT_URL, CLIENT, HTTPStatus.FOUND),
    )
)
def test_pages_availability_for_anonymous_user(client_fixure, url, status):
    assert client_fixure.get(url).status_code == status


@pytest.mark.parametrize(
    'url, redirect',
    (
        (DELETE_URL, REDIRECT_DELETE_URL),
        (EDIT_URL, REDIRECT_EDIT_URL),
    )
)
def test_availability_for_comment_edit_and_delete(url, redirect, client):
    assertRedirects(client.get(url), redirect)
