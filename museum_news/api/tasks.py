from celery import shared_task
from utils.wp_checker import NewsCollector

from .models import News


@shared_task
def collect_news(per_page: int) -> None:
    """Собирает новости с сайтов в базу."""

    collector = NewsCollector()
    collector.get_urls()
    for url in collector.urls:
        print(url)
        data = collector.get_news(url, per_page)
        if data == []:
            continue
        for post in data:
            news = News.objects.all()
            title = post['title']
            url = post['url']
            if news.filter(url=url, title=title).exists():
                continue
            try:
                News.objects.create(
                    title=post['title'],
                    news=post['post'],
                    url=post['url']
                )
            except Exception as e:
                print('Ошибка записи в БД: ', e)
    print('Collecting finished')
