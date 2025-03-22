from notes.forms import NoteForm
from notes.tests.testing_utils import (
    FixtureCase,
    LIST_URL,
    ADD_URL,
    EDIT_URL
)


class TestContent(FixtureCase):
    def test_note_in_list(self):
        notes = self.author_client.get(LIST_URL).context['object_list']
        self.assertIn(self.note, notes)
        note = notes.get(pk=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_note_not_in_list(self):
        self.assertNotIn(
            self.note,
            self.not_author_client.get(LIST_URL).context['object_list']
        )

    def test_pages_contains_form(self):
        urls = (ADD_URL, EDIT_URL)
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
