from django.contrib.auth.models import User
from django.db import models


DEFAULT_PROJECT_STATUS = 'common'
PROJECT_STATUS_CHOICES = [(DEFAULT_PROJECT_STATUS, 'Общий'), ('hide', 'Скрытый'), ('private', 'Приватный')]


# Create your models here.
class File(models.Model):
    file = models.FileField(null=False, blank=False, upload_to='user_files', verbose_name='Файл')
    description = models.CharField(max_length=120, verbose_name='Описание файла', null=False, blank=False)
    created_by = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name='Автор объявления')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    downloaded = models.IntegerField(default=0, verbose_name='Количество скачиваний')
    access = models.CharField(choices=PROJECT_STATUS_CHOICES, default=DEFAULT_PROJECT_STATUS, verbose_name='Доступ', max_length=20)


class FilePrivate(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)