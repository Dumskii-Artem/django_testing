# notes/tests/testing_utils.py

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


NOTE_SLUG = 'note_slug'

HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))


class FixtureCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.auth_user = User.objects.create(username='Авторизированный')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.auth_user)

        cls.author_user = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author_user)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=NOTE_SLUG,
            author=cls.author_user
        )

        cls.note_data = {
            'title': 'Второй заголовок',
            'text': 'Второй текст',
            'slug': 'second-slug'
        }
