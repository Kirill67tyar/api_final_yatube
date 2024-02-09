from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь подписан'
    )
    following = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='На пользователя подписан'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following', ],
                name='unique_key_user_following'
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user=models.F('following')),
            ),
        ]

    def __str__(self):
        user = self._meta.fields[1].name
        following = self._meta.fields[-1].name
        return f'{user} - {following} ({self.user_id}, {self.following_id})'


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
