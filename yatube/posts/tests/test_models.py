from django.test import TestCase
from posts.models import Group, Post, User


class ModelTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """ Создание записи в БД. """
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='test_slug_group',
            description='Тестовое описание группы'
        )

        cls.user = User.objects.create(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def test_group_str(self):
        group_obj = ModelTests.group
        excepted_obj_name = group_obj.title
        self.assertEqual(excepted_obj_name, str(group_obj))

    def test_post_str(self):
        post_obj = ModelTests.post
        expected_obj_name = post_obj.text[:15]
        self.assertEqual(expected_obj_name, str(post_obj)[:15])

    def test_post_verbose_name(self):
        post = ModelTests.post
        field_verbose = {
            'text': 'Текст поста',
            'pub_date': 'Дата',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value
                )
