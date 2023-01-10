from django import forms

from .models import Post,Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст',
            'group': 'Группа',
            'image': 'Картинка'
        }
        help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите значение из выпадающего списка',
            'image': 'Загрузите изображение'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            # 'post',
            'text'
        )
