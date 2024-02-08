from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='select_followers',
        verbose_name='Пользователь подписан'
    )
    following = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='select_followings',
        verbose_name='На пользователя подписан'
    )

    def __str__(self):
        return f'{self.pk}) Связь подписчиков'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following', ],
                name='unique_key_user_following'
            ),
        ]


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        to='posts.Group',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        default_related_name = 'posts'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
