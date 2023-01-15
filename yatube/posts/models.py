from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
NUMB_SYBM = 30


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        help_text='Группа, к которой будет относится пост'
    )

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'posts_rname'

    def __str__(self):
        return self.text[:NUMB_SYBM]
