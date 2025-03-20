import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects
from django.test.client import Client
from http import HTTPStatus

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

pytestmark = pytest.mark.django_db
client = Client()

COMMENT_TEXT = 'Новый текст'
COMMENT_DATA = {
    'text': COMMENT_TEXT
}

BAD_COMMENT_TEXT = f'** ****** hhhhh {BAD_WORDS[0]} hhhhhhhhhhh'
BAD_COMMENT_DATA = {
    'text': BAD_COMMENT_TEXT
}


def test_anonymous_user_cant_create_comment(client, news):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=COMMENT_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(not_author_client, news, not_author):
    url = reverse('news:detail', args=(news.id,))
    not_author_client.post(url, data=COMMENT_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news, news
    assert comment.author, not_author


def test_user_cant_use_bad_words(not_author_client, news, not_author):
    url = reverse('news:detail', args=(news.id,))
    response = not_author_client.post(url, data=BAD_COMMENT_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 0
    form = response.context['form']
    assert 'text' in form.errors
    assert WARNING in form.errors['text']


def test_author_can_delete_comment(author_client, news, comment):
    url = reverse('news:delete', args=(comment.id,))
    author_client.post(url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_not_author_cant_delete_comment(not_author_client, news, comment):
    url = reverse('news:delete', args=(comment.id,))
    not_author_client.post(url)
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client, news, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=COMMENT_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    redirect_url = reverse('news:detail', args=(comment.id,)) + '#comments'
    assertRedirects(response, redirect_url)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == COMMENT_TEXT
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author


def test_not_author_cant_edit_comment(not_author_client, news, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, data=COMMENT_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    assert response.status_code == HTTPStatus.NOT_FOUND
    not_updated_comment = Comment.objects.get(pk=comment.pk)
    assert not_updated_comment.text == comment.text
