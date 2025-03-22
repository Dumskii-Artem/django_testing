from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


NOTE_SLUG = 'note_slug'

ADD_URL = reverse('notes:add')
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))

REDIRECT_ADD_URL = f'{LOGIN_URL}?next={ADD_URL}'
REDIRECT_DELETE_URL = f'{LOGIN_URL}?next={DELETE_URL}'
REDIRECT_DETAIL_URL = f'{LOGIN_URL}?next={DETAIL_URL}'
REDIRECT_EDIT_URL = f'{LOGIN_URL}?next={EDIT_URL}'
REDIRECT_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
REDIRECT_SUCCESS_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'


class FixtureCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.not_author_user = User.objects.create(username='Авторизированный')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author_user)

        cls.author_user = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author_user)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=NOTE_SLUG,
            author=cls.author_user
        )

        cls.form_data = {
            'title': 'Второй заголовок',
            'text': 'Второй текст',
            'slug': 'second-slug'
        }

        cls.form_data_empty_slug = {
            'title': 'Третий заголовок',
            'text': 'Третий текст',
            'slug': ''
        }

