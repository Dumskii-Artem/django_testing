import pytest
from django.test.client import Client

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE

pytestmark = pytest.mark.django_db
client = Client()


def test_news_count_on_page(news_sample, home_url):
    assert client.get(
        home_url).context['object_list'].count() == NEWS_COUNT_ON_HOME_PAGE


def test_news_sorting(news_sample, client, home_url):
    all_dates = [news.date
                 for news in client.get(home_url).context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_sorting(comments_sample, client, news, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    all_timestamps = [comment.created
                      for comment
                      in response.context['news'].comment_set.all()]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client, news, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(not_author_client, news, detail_url):
    assert isinstance(
        not_author_client.get(detail_url).context.get('form'),
        CommentForm
    )
