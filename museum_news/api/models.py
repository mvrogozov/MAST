from django.db import models


class News(models.Model):
    url = models.CharField(
        'Адрес сайта',
        max_length=128
    )
    title = models.CharField(
        'Заголовок',
        max_length=256
    )
    news = models.TextField(
        'Новость',
        max_length=10000
    )

    class Meta:
        ordering = ('title',)
