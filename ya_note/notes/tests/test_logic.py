from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.tests.testing_utils import (
    FixtureCase,
    NOTE_SLUG,

    ADD_URL,
    SUCCESS_URL,
    EDIT_URL,
    DELETE_URL
)


class TestLogic(FixtureCase):
    def test_anonimus_user_cant_create_note(self):
        notes_before = set(Note.objects.all())
        self.client.post(ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        notes_before = set(Note.objects.all())
        self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertEqual(set(Note.objects.all()), notes_before)

    # + test_empty_slug_filled_with_title
    def test_auth_user_can_create_note(self):
        cases = (
            [self.form_data['slug'], self.form_data['slug']],
            ['', slugify(self.form_data['title'])],
        )
        for form_slug, result_slug in cases:
            with self.subTest(form_slug=form_slug):
                self.form_data['slug'] = form_slug
                notes_before = set(Note.objects.all())
                self.auth_client.post(ADD_URL, data=self.form_data)
                created_notes = set(Note.objects.all()) - notes_before
                self.assertEqual(len(created_notes), 1)
                new_note = created_notes.pop()
                self.assertEqual(new_note.title, self.form_data['title'])
                self.assertEqual(new_note.text, self.form_data['text'])
                self.assertEqual(new_note.slug, result_slug)
                self.assertEqual(new_note.author, self.auth_user)

    def test_author_can_edit_note(self):
        note_id = self.note.id
        self.assertRedirects(
            self.author_client.post(EDIT_URL, data=self.form_data),
            SUCCESS_URL
        )
        new_note = Note.objects.get(id=note_id)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.author, self.author_user)

    def test_author_can_delete_note(self):
        notes_before = set(Note.objects.all())
        self.assertRedirects(self.author_client.post(DELETE_URL), SUCCESS_URL)
        deleted_notes = notes_before - set(Note.objects.all())
        self.assertEqual(len(deleted_notes), 1)
        deleted_note = deleted_notes.pop()
        self.assertEqual(deleted_note.title, self.note.title)
        self.assertEqual(deleted_note.text, self.note.text)
        self.assertEqual(deleted_note.slug, self.note.slug)
        self.assertEqual(deleted_note.author, self.author_user)

    def test_not_author_cant_edit_note(self):
        response = self.auth_client.post(EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # данные не сохранились
        new_note = Note.objects.get(slug=NOTE_SLUG)
        self.assertEqual(new_note.text, self.note.text)
        self.assertEqual(new_note.title, self.note.title)

    def test_auth_cant_delete_note(self):
        response = self.auth_client.post(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
