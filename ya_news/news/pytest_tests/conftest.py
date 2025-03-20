# conftest.py
from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.utils import timezone

from news.models import News, Comment


from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def news(db):
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(author, news, db):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def news_sample(db):
    News.objects.bulk_create(
        News(
            title=f'Заголовок {index + 1}',
            text=f'Текст заметки {index + 1}',
            date=datetime.today() - timedelta(days=index)
        ) for index in range(NEWS_COUNT_ON_HOME_PAGE)
    )


@pytest.fixture
def comments_sample(author, news, db):
    for index in range(15):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст комментария {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
