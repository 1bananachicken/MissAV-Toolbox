import os
import requests
import cloudscraper
from bs4 import BeautifulSoup
from missav_toolbox.type_enum import MovieType, SortBy


class BaseDownloader:
    def __init__(self, save_path: str, movie_type=MovieType.professional, sort_by=SortBy.ReleaseDate,
                 keywords=None):
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        self.base_save_path = save_path
        self.save_path = None

        if os.environ.get('http_proxy') is not None and os.environ.get('https_proxy') is not None:
            self.proxy = {'http': os.environ.get('http_proxy'), 'https': os.environ.get('https_proxy')}
        else:
            self.proxy = None

        self.movie_type = movie_type
        self.sort_by = sort_by

        self.keywords = self.parse_keywords(keywords)

        self.prefix = 'https://missav.com/dm16/cn/'
        self.types = ['release', 'fc2', 'search/']
        self.suffix = '&page='
        self.all_sort_by = ['?sort=released_at', '?sort=published_at', '?sort=today_views', '?sort=weekly_views',
                            '?sort=monthly_views']

        self.link = f'{self.prefix}{self.types[self.movie_type.value]}{self.keywords}{self.all_sort_by[self.sort_by.value]}'

        self.scraper = self.get_scraper()

        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36",
            'headerser': 'https://google.com'}

    @staticmethod
    def get_scraper():
        return cloudscraper.create_scraper(delay=5, browser={'browser': 'chrome',
                                                             'platform': 'windows',
                                                             'mobile': False})

    def get_page_parser(self, link, page=None):
        try:
            if page is not None:
                link += f'{self.suffix}{page}'
            content = self.scraper.get(link, proxies=self.proxy, headers=self.headers)
            content.raise_for_status()
        except requests.exceptions.HTTPError:
            raise requests.HTTPError('Can\'t fetch the content')

        return BeautifulSoup(content.text, 'html.parser')

    def get_num_pages(self):
        try:
            num_pages = int(
                self.get_page_parser(self.link, 1).find_all('a', class_='relative')[-2].contents[0].split('\n')[1])
        except IndexError:
            num_pages = 1

        return num_pages

    def get_all_videos(self, page=1):
        return self.get_page_parser(self.link, page).find_all('a', class_='text-secondary group-hover:text-primary')

    def parse_keywords(self, keywords):
        if keywords is None:
            if self.movie_type == MovieType.search:
                raise ValueError('Keywords should be provided for search type')
            return ''
        elif isinstance(keywords, str):
            self.movie_type = MovieType.search
            return keywords
        elif isinstance(keywords, list):
            self.movie_type = MovieType.search
            return '+'.join(keywords)
        else:
            raise ValueError('Keywords should be a string or a list of strings')

    def download(self):
        pass
