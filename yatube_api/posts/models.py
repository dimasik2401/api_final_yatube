from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Group(models.Model):
    """Модель для группы сообщества."""
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для поста."""
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор')
    image = models.ImageField(
        upload_to='posts/', blank=True, verbose_name='Изображение')
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='posts',
                              blank=True,
                              null=True,
                              verbose_name='Группа')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.text) > 50 else self.text


class Comment(models.Model):
    """Модель для комментария."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments',
        verbose_name='Автор')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    """Модель для подписок пользователей друг на друга."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = [['user', 'following']]

    def clean(self):
        if self.user == self.following:
            raise ValidationError("Невозможно подписаться на самого себя.")

    def __str__(self):
        return str(self.user)
