import csv
import json

import requests


FILENAME = 'museums-urls.csv'
ROW_TITLE = '_source/general/contacts/website'


def get_urls(filename: str, row_title:str) -> list:
    urls = []
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            urls.append(row[row_title])
    return urls


def strip_tags(string: str):  # TODO
    import re
    # as per recommendation from @freylis, compile once only
    CLEANR = re.compile('(<.*?>)|(&nbsp;)|(\n)')#('<.*?>')
    cleantext = re.sub(CLEANR, '', string)
    return cleantext


def get_news(urls: list):
    wp_api_url = '/wp-json/wp/v2/posts/?per_page=1'
    for url in urls[:25]:
        try:
            response = requests.get(url + wp_api_url)
            if response.headers['Content-Type'].startswith('application/json'):
                print(url, ' -> ', response.headers['Content-Type'])
                a = json.loads(response.content)
                print('title =   ', a[0]['title']['rendered'])
                print('content =   ', a[0]['content']['rendered'])
                print('LET ME SEE YOU STRIPPED: ',  strip_tags(a[0]['content']['rendered']))

        except Exception as e:
            pass
            #print(f'Ошибка при запросе к {url}: {e}')


def main():
    urls = get_urls(FILENAME, ROW_TITLE)
    get_news(urls)


if __name__ == '__main__':
    main()
