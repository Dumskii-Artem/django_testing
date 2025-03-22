from http import HTTPStatus

import pytest
from django.test.client import Client
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db
client = Client()

COMMENT_DATA = {'text': 'Новый текст'}

BAD_COMMENT_DATA = [
    {'text': f'** ***, *** hhhhh {bad_word} hhhhh. hhh'}
    for bad_word in BAD_WORDS
]


def test_anonymous_user_cant_create_comment(client, detail_url):
    assert client.post(
        detail_url, data=COMMENT_DATA
    ).status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        not_author_client,
        news,
        not_author,
        detail_url
):
    assert not_author_client.post(
        detail_url, data=COMMENT_DATA
    ).status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_DATA['text']
    assert comment.news == news
    assert comment.author == not_author


@pytest.mark.parametrize(
    'data_with_bad_word', BAD_COMMENT_DATA
)
def test_user_cant_use_bad_words(
        not_author_client,
        detail_url,
        data_with_bad_word
):
    response = not_author_client.post(detail_url, data=data_with_bad_word)
    assert response.status_code == HTTPStatus.OK
    assert Comment.objects.count() == 0
    form = response.context['form']
    assert 'text' in form.errors
    assert WARNING in form.errors['text']


def test_author_can_delete_comment(author_client, news, comment, delete_url):
    assert author_client.post(delete_url).status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_not_author_cant_delete_comment(
        not_author_client,
        delete_url,
        comment
):
    assert not_author_client.post(
        delete_url).status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    assert Comment.objects.filter(pk=comment.pk).exists()
    current_comment = Comment.objects.get(pk=comment.pk)
    assert comment.text == current_comment.text
    assert comment.news == current_comment.news
    assert comment.author == current_comment.author


def test_author_can_edit_comment(
        author_client,
        comment,
        edit_url,
        redirect_detail_comments
):
    response = author_client.post(edit_url, data=COMMENT_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
    assertRedirects(response, redirect_detail_comments)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == COMMENT_DATA['text']
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author


def test_not_author_cant_edit_comment(not_author_client, comment, edit_url):
    response = not_author_client.post(edit_url, data=COMMENT_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    assert response.status_code == HTTPStatus.NOT_FOUND
    not_updated_comment = Comment.objects.get(pk=comment.pk)
    assert not_updated_comment.text == comment.text
    assert not_updated_comment.news == comment.news
    assert not_updated_comment.author == comment.author
