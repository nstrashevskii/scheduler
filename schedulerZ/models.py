from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


def in_next_days():
    return timezone.now() + timedelta(days=1)


class Notes(models.Model):
    STATUS = (
        (0, 'Активно'),
        (1, 'Отложено'),
        (2, 'Выполнено'),
    )

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    message = models.TextField(default='', verbose_name='Текст')
    date = models.DateTimeField(default=in_next_days, verbose_name='Время выполнения')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    important = models.BooleanField(default=False, verbose_name='Важно')
    author = models.ForeignKey(User, related_name='authors', on_delete=models.PROTECT, blank=True)
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='Статус')

    def __str__(self):
        return self.title

# Create your models here.
