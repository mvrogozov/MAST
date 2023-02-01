from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.wp_checker import NewsCollector


from .serializers import NewsSerializer
from .models import News


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CollectNewsView(APIView):
    def get(self, request):
        """Собирает новости с сайтов в базу."""
        collector = NewsCollector()
        data = collector.collect_news()
        unique_data = []
        news = News.objects.all()
        for item in data:
            title = item['title']
            url = item['url']
            if news.filter(url=url, title=title).exists():
                continue
            unique_data.append(item)

        News.objects.bulk_create(
            [
                News(
                    title=item['title'],
                    news=item['post'],
                    url=item['url']
                ) for item in unique_data
            ]
        )
        return Response('Done')
