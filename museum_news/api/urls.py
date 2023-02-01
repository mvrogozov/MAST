from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsViewSet, CollectNewsView


router = DefaultRouter()
router.register('news', NewsViewSet, basename='api_news')

urlpatterns = [
    path('', include(router.urls), name='api_news_list'),
    path('collect/', CollectNewsView.as_view(), name='api_collect')
]
