import csv
import json
import re

import requests

from api.models import NEWS_LENGTH, TITLE_LENGTH


class NewsCollector():
    FILENAME = 'museums-urls.csv'
    ROW_TITLE = '_source/general/contacts/website'

    def __init__(self, filename: str = FILENAME, row_title: str = ROW_TITLE):
        self.urls = []
        self.filename = filename
        self.row_title = row_title
        self.is_running = False

    def get_urls(
        self,
        filename: str = FILENAME,
        row_title: str = ROW_TITLE
    ) -> list:
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                self.urls.append(row[row_title])

    @classmethod
    def strip_tags(cls, string: str):
        """Убирает html теги, пробелы, символы переноса строки"""
        CLEANR = re.compile('(<.*?>)|(&nbsp;)|(\n)')
        cleartext = re.sub(CLEANR, '', string)
        return cleartext

    def get_news(self, url: str, per_page: int) -> list:
        """Проверка, если сайт на wordpress, собираем результат"""
        wp_api_url = f'/wp-json/wp/v2/posts/?per_page={per_page}'
        result = []
        try:
            response = requests.get(url + wp_api_url, timeout=5)
            if response.headers['Content-Type'].startswith(
                'application/json'
            ):
                content = json.loads(response.content)
                for post in content:
                    result.append({
                        'title': post['title']['rendered'][:TITLE_LENGTH],
                        'post': self.strip_tags(
                            post['content']['rendered'][:NEWS_LENGTH]
                        ),
                        'url': url
                    })
        except Exception:
            return []
        return result
