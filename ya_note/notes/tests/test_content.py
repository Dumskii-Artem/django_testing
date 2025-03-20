# notes/tests/test_content.py

from django.conf import settings

from notes.tests.testing_utils import (
    FixtureCase,
    LIST_URL,
    ADD_URL,
    EDIT_URL
)


class TestContent(FixtureCase):
    def test_note_in_list(self):
        response = self.author_client.get(LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_not_in_list(self):
        response = self.auth_client.get(LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_pages_contains_form(self):
        urls = (ADD_URL, EDIT_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
