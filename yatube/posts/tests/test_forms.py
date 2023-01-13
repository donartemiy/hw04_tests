# posts/tests/tests_form.py
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """ Создание записи в БД. """
        super().setUpClass()
        cls.test_user = User.objects.create_user(username='TestUser')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.test_user)

        cls.group1 = Group.objects.create(
            title='Тестовый заголовок группы 1',
            slug='test_slug_group_1',
            description='Тестовое описание группы 1'
        )
        cls.group2 = Group.objects.create(
            title='Тестовый заголовок группы 2',
            slug='test_slug_group_2',
            description='Тестовое описание группы 2'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст поста 1',
            author=cls.test_user,
            group=cls.group1
        )

    def test_post_create(self):
        """ Форма создает запись в Post. """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст поста 2',
            'group': PostFormTests.group1.id
        }
        # Отправляем POST-запрос
        response = PostFormTests.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostFormTests.test_user})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с заданным текстом
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст поста 2'
            ).exists()
        )

    def test_post_edit(self):
        """ Изменение текста и группы при отправке валидной формы. """
        form_data = {
            'text': 'Текст изменён',
            'group': PostFormTests.group2.id
        }
        # Отправляем POST-запрос
        response = PostFormTests.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostFormTests.post.pk}
            ),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Проверяем, что текст изменился
        self.assertEqual(
            Post.objects.get(pk=PostFormTests.post.pk).text,
            form_data['text'])
        # Проверяем, что группа изменился
        self.assertEqual(
            Post.objects.get(pk=PostFormTests.post.pk).group.id,
            form_data['group'])
