from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from utils.wp_checker import NewsCollector


from .serializers import NewsSerializer
from .models import News


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'news')


class CollectNewsView(APIView):
    def get(self, request):
        """Собирает новости с сайтов в базу."""
        collector = NewsCollector()
        collector.get_urls()
        for url in collector.urls:
            data = collector.get_news(url, 10)
            if not data:
                continue
            news = News.objects.all()
            title = data['title']
            url = data['url']
            if news.filter(url=url, title=title).exists():
                continue
            #unique_data.append(item)

            News.objects.create(
                title=data['title'],
                news=data['post'],
                url=data['url']
            )
        return Response('Done')
