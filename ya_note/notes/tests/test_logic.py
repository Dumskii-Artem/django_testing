# notes/tests/test_logic.py

from django.conf import settings
from django.urls import reverse
from pytils.translit import slugify
from http import HTTPStatus

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
        self.client.post(ADD_URL, data=self.note_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_auth_user_can_create_note(self):
        self.auth_client.post(ADD_URL, data=self.note_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)

        new_note = Note.objects.get(slug=self.note_data['slug'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.title, self.note_data['title'])

    def test_not_unique_slug(self):
        self.note_data['slug'] = NOTE_SLUG
        self.auth_client.post(ADD_URL, data=self.note_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_empty_slug_filled_with_title(self):
        self.note_data['slug'] = ''
        self.auth_client.post(ADD_URL, data=self.note_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)

        new_note = Note.objects.get(slug=slugify(self.note_data['title']))
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.title, self.note_data['title'])

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_URL, data=self.note_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_note = Note.objects.get(slug=self.note_data['slug'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.title, self.note_data['title'])

    def test_author_can_delete_note(self):
        response = self.author_client.post(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_auth_cant_edit_note(self):
        response = self.auth_client.post(EDIT_URL, data=self.note_data)
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
