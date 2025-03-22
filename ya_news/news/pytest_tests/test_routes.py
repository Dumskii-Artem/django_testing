# test_routes.py
import pytest
# from pytest import lazy_fixture
from pytest_django.asserts import assertRedirects
from http import HTTPStatus

from django.urls import reverse
from django.test.client import Client

HOME_URL = pytest.lazy_fixture('home_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
EDIT_URL = pytest.lazy_fixture('edit_url')

REDIRECT_DELETE_URL = pytest.lazy_fixture('redirect_delete_url')
REDIRECT_EDIT_URL = pytest.lazy_fixture('redirect_edit_url')

AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')

pytestmark = pytest.mark.django_db
client = Client()


@pytest.mark.parametrize(
    'url, client, status',
    (
        (HOME_URL, client, HTTPStatus.OK),

        (LOGIN_URL, client, HTTPStatus.OK),
        (LOGOUT_URL, client, HTTPStatus.OK),
        (SIGNUP_URL, client, HTTPStatus.OK),
        (DETAIL_URL, client, HTTPStatus.OK),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_anonymous_user(client, url, status):
    assert client.get(url).status_code == status


@pytest.mark.parametrize(
    'url, redirect',
    (
        (DELETE_URL, REDIRECT_DELETE_URL),
        (EDIT_URL, REDIRECT_EDIT_URL),
    )
)
def test_availability_for_comment_edit_and_delete(url, redirect, client):
    assertRedirects(client.get(url), redirect)
