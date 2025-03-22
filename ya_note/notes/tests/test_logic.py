from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.tests.testing_utils import (
    FixtureCase,

    ADD_URL,
    SUCCESS_URL,
    EDIT_URL,
    DELETE_URL
)


class TestLogic(FixtureCase):
    def test_anonim_user_cant_create_note(self):
        notes = set(Note.objects.all())
        self.client.post(ADD_URL, data=self.form_data)
        self.assertEqual(notes, set(Note.objects.all()))

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        notes = set(Note.objects.all())
        self.not_author_client.post(ADD_URL, data=self.form_data)
        self.assertEqual(set(Note.objects.all()), notes)

    def create_note_and_check(self, form_data, result_slug):
        notes = set(Note.objects.all())
        self.not_author_client.post(ADD_URL, data=form_data)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.slug, result_slug)
        self.assertEqual(note.author, self.not_author_user)

    # + test_empty_slug_filled_with_title
    def test_auth_user_can_create_note(self):
        self.create_note_and_check(
            self.form_data,
            self.form_data['slug']
        )

        self.create_note_and_check(
            self.form_data_empty_slug,
            slugify(self.form_data_empty_slug['title'])
        )

    def test_author_can_edit_note(self):
        self.assertRedirects(
            self.author_client.post(EDIT_URL, data=self.form_data),
            SUCCESS_URL
        )
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.slug, self.form_data['slug'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        self.assertRedirects(self.author_client.post(DELETE_URL), SUCCESS_URL)
        self.assertEqual(notes_count - Note.objects.count(), 1)
        self.assertNotIn(self.note, Note.objects.all())

    def test_not_author_cant_edit_note(self):
        self.assertEqual(
            self.not_author_client.post(
                EDIT_URL,
                data=self.form_data
            ).status_code,
            HTTPStatus.NOT_FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_not_author_cant_delete_note(self):
        notes = set(Note.objects.all())
        self.assertEqual(
            self.not_author_client.post(DELETE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(notes, set(Note.objects.all()))

        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
