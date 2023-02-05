from django.contrib import admin

from api.models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'url',
        'title',
        'news',
    )
    search_fields = ('url', 'title', 'news')
    list_filter = ('url', 'title', 'news')
    empty_value_display = '-пусто-'


admin.site.register(News, NewsAdmin)
