from django.db import models

TITLE_LENGTH = 256
NEWS_LENGTH = 10000


class News(models.Model):
    url = models.CharField(
        'Адрес сайта',
        max_length=128
    )
    title = models.CharField(
        'Заголовок',
        max_length=TITLE_LENGTH
    )
    news = models.TextField(
        'Новость',
        max_length=NEWS_LENGTH
    )

    class Meta:
        ordering = ('url',)
