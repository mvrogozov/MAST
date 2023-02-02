from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import News
from .serializers import NewsSerializer
from .tasks import collect_news


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'news')


class CollectNewsView(APIView):
    def get(self, request):
        task = collect_news.apply_async((10,))
        return Response({"task_id": task.id}, 200)
