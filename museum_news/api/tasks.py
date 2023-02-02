from celery import shared_task
from utils.wp_checker import NewsCollector

from .models import News


@shared_task
def collect_news(per_page: int) -> None:
    """Собирает новости с сайтов в базу."""
    collector = NewsCollector()
    collector.get_urls()
    for url in collector.urls:
        data = collector.get_news(url, per_page)
        if not data:
            continue
        news = News.objects.all()
        title = data['title']
        url = data['url']
        if news.filter(url=url, title=title).exists():
            continue
        News.objects.create(
            title=data['title'],
            news=data['post'],
            url=data['url']
        )
