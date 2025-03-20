# test_routes.py
import pytest
# from pytest import lazy_fixture
from pytest_django.asserts import assertRedirects
from http import HTTPStatus

from django.urls import reverse
from django.test.client import Client

pytestmark = pytest.mark.django_db
client = Client()


# test_routes.py
@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_page_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_availability_for_comment_edit_and_delete(
    name,
    author_client,
    comment
):
    url = reverse(name, args=(comment.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_availability_for_comment_edit_and_delete(name, client, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_availability_for_comment_edit_and_delete_not_author(
        name, not_author_client, comment
):
    url = reverse(name, args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
