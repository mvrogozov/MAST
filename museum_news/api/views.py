from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from utils.wp_checker import NewsCollector
from .tasks import collect_news


from .serializers import NewsSerializer
from .models import News


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'news')


class CollectNewsView(APIView):
    def get(self, request):
        task = collect_news.apply_async()
        return Response({"task_id": task.id}, 200)
