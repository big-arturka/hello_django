from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


TOKEN_TYPE_REGISTER = 'register'
TOKEN_TYPE_PASSWORD_RESET = 'password_reset'
TOKEN_TYPE_CHOICES = (
    (TOKEN_TYPE_REGISTER, 'Регистрация'),
    (TOKEN_TYPE_PASSWORD_RESET, 'Восстановление пароля')
)


class AuthToken(models.Model):
    token = models.UUIDField(verbose_name='Токен', default=uuid4)
    user: AbstractUser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                           related_name='tokens', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    life_days = models.IntegerField(default=7, verbose_name='Срок действия (в днях)')
    type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES,
                            default=TOKEN_TYPE_REGISTER, verbose_name='Тип токена')

    @classmethod
    def get_token(cls, token):
        try:
            return cls.objects.get(token=token)
        except cls.DoesNotExist:
            return None

    def is_alive(self):
        return (self.created_at + timedelta(days=self.life_days)) >= now()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Аутентификационный токен'
        verbose_name_plural = 'Аутентификационные токены'


class Profile(models.Model):
    user: AbstractUser = models.OneToOneField(get_user_model(), related_name='profile',
                                              on_delete=models.CASCADE, verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
