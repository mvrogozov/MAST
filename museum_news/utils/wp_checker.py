import csv
import json
import re

import requests


class NewsCollector():
    FILENAME = 'museums-urls.csv'
    ROW_TITLE = '_source/general/contacts/website'

    def __init__(self):
        self.urls = []

    def get_urls(
        self,
        filename: str = FILENAME,
        row_title: str = ROW_TITLE
    ) -> list:
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                self.urls.append(row[row_title])
        return self.urls

    @classmethod
    def strip_tags(cls, string: str):
        CLEANR = re.compile('(<.*?>)|(&nbsp;)|(\n)')
        cleartext = re.sub(CLEANR, '', string)
        return cleartext

    def get_news(self, per_page: int):
        wp_api_url = f'/wp-json/wp/v2/posts/?per_page={per_page}'
        result = []
        for url in self.urls[:50]:
            try:
                response = requests.get(url + wp_api_url)
                if response.headers['Content-Type'].startswith(
                    'application/json'
                ):
                    content = json.loads(response.content)
                    for post in content:
                        result.append({
                            'title': post['title']['rendered'],
                            'post': self.strip_tags(
                                post['content']['rendered']
                            ),
                            'url': url
                        })
            except Exception as e:
                print(f'Ошибка при запросе к {url}: {e}')
        print('\n\nDONE')
        return result

    def collect_news(self, per_page: int = 10):
        self.get_urls()
        return self.get_news(per_page)
