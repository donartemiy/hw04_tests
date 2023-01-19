from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase

from posts.models import Group, Post, User


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """ Создание записи в БД. """
        super().setUpClass()
        cls.test_user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='test_slug_group',
            description='Тестовое описание группы'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.test_user,
            group=cls.group
        )

    def setUp(self):
        cache.clear()

    def test_url_200_unknonw_user(self):
        routes = [
            '/',
            f'/group/{StaticURLTests.post.group.slug}/',
            f'/profile/{StaticURLTests.post.author}/',
            f'/posts/{StaticURLTests.post.pk}/',
        ]
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_200_knonw_user(self):
        self.client.force_login(StaticURLTests.test_user)
        routes = [
            f'/posts/{StaticURLTests.post.pk}/edit/',
            '/create/'
        ]
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_404(self):
        """ Неавторизованный пользователь не может
        редактировать и создавать пост. """
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_302_unknonw_user(self):
        response = self.client.get(
            f'/posts/{StaticURLTests.post.pk}/edit/'
        )

        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{StaticURLTests.post.pk}/edit/'
        )

        response = self.client.get('/create/')
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_url_302_knonw_user(self):
        self.test_user2 = User.objects.create_user(username='TestUser2')
        self.client.force_login(self.test_user2)
        response = self.client.get(
            f'/posts/{StaticURLTests.post.pk}/edit/'
        )

        self.assertRedirects(response, f'/posts/{StaticURLTests.post.pk}/')

    def test_urls_uses_correct_temp(self):
        self.client.force_login(StaticURLTests.test_user)
        urls_templates_names = {
            '/': 'posts/index.html',
            f'/group/{StaticURLTests.post.group.slug}/':
            'posts/group_list.html',

            f'/profile/{StaticURLTests.post.author}/': 'posts/profile.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{StaticURLTests.post.pk}/': 'posts/post_detail.html',
            f'/posts/{StaticURLTests.post.pk}/edit/': 'posts/create_post.html'
        }
        for url, template in urls_templates_names.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
