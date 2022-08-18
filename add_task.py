import requests
import bs4
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415;'
              ' _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2;'
              ' __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}

base_url = 'https://habr.com'
url = base_url + '/ru/all/'

KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def responce_get(urls, headers):
    """Поиск статей по содержимому страницы сайта"""
    response = requests.get(url=urls, headers=headers)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    return articles


def find_link(articles, base_urls):
    """Поиск ссылок на статьи с главной страницы"""
    href = articles.find(class_='tm-article-snippet__title-link').attrs['href']
    links = base_urls + href
    return links


def keyword_search(articles, keywords):
    """Поиск ключевых слов по всему тексту статьи"""
    for article in articles:
        text_blocks = article.find(class_='tm-article-body')
        text_blocks = set(text_block.text.strip() for text_block in text_blocks)
        for text_block in text_blocks:
            text_block = re.sub(r'[.,!?/]', ' ', text_block)
            text_block = text_block.split()
            hub_list = []
            for word in text_block:
                next_hub = morph.parse(word)[0].normal_form
                hub_list.append(next_hub)
            if set(keywords) & set(hub_list):
                title = article.find('h1').find('span').text
                hub_datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                hub_date, hub_time = hub_datetime.split(', ')
                result = hub_date + ' - ' + title + ' - ' + link
                print(result)
                return result


if __name__ == '__main__':

    hubs = responce_get(url, HEADERS)
    for hub in hubs:  #
        link = find_link(hub, base_url)
        hub_articles = responce_get(link, HEADERS)
        keyword_search(hub_articles, KEYWORDS)
