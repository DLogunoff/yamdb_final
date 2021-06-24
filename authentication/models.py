from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        db_index=True,
        max_length=230,
        unique=True,
        verbose_name='Имя пользователя'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    is_staff = models.BooleanField(default=False, verbose_name='Модератор')
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата регистрации'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    user_role_choice = models.CharField(
        max_length=15,
        choices=USER_ROLES,
        verbose_name='Роль'
    )

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Код подтверждения'
    )
    role = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Роль'

    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    first_name = models.CharField(
        blank=True,
        max_length=230,
        unique=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        blank=True,
        max_length=230,
        unique=False,
        verbose_name='Фамилия'
    )

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def is_admin(self):
        return (self.role == self.ADMIN) or self.is_staff

    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def token(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
