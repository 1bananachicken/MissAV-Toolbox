import io
import requests
import os
from missav_toolbox.base_downloader import BaseDownloader
from PIL import Image, ImageFont, ImageDraw
from missav_toolbox.type_enum import MovieType, SortBy


class CoverDownloader(BaseDownloader):
    """
    Download movie covers from missav.com and make a collage

    :param save_path: str, the path to save the covers
    :param movie_type: professional, fc2, search
    :param sort_by: ReleaseDate, RecentUpdate, TodayViews, WeeklyViews, MonthlyViews
    """

    def __init__(self, save_path='covers', movie_type=MovieType.professional, sort_by=SortBy.ReleaseDate,
                 keywords=None):
        super().__init__(save_path, movie_type, sort_by, keywords)

        self.count = 0
        self.top_covers = {}
        self.top_ids = {}

    def download_cover(self, movie_title, movie_id):
        # fix the bug that the movie title contains '/?*\'
        movie_title = movie_title.replace('/', '')
        movie_title = movie_title.replace('*', '')
        movie_title = movie_title.replace('?', '')
        movie_title = movie_title.replace('\\', '')

        cover_save_path = os.path.join(self.save_path, f'{movie_title}.jpg')
        if os.path.exists(cover_save_path):
            if self.count < 10:
                with open(cover_save_path, 'rb') as f:
                    self.top_covers[self.count] = f.read()
                self.top_ids[self.count] = movie_id.upper()
                self.count += 1
            return

        print(f'Downloading cover: {movie_title}')

        try:
            movie_cover_link = f'https://fivetiu.com/{movie_id}/cover-n.jpg'
            cover = self.scraper.get(movie_cover_link, proxies=self.proxy, headers=self.headers)
            cover.raise_for_status()
            with open(cover_save_path, 'wb') as f:
                f.write(cover.content)
        except requests.exceptions.HTTPError:
            # try to download low resolution cover
            movie_cover_link = f'https://fivetiu.com/{movie_id}/cover-t.jpg'
            cover = self.scraper.get(movie_cover_link, proxies=self.proxy, headers=self.headers)
            with open(cover_save_path, 'wb') as f:
                f.write(cover.content)

        # get top10 movies
        if self.count < 10:
            self.top_covers[self.count] = cover.content
            self.top_ids[self.count] = movie_id.upper()

        self.count += 1

    def show_top10(self):
        x_offset = 20
        y_offset = 100
        background_width = 1660
        background_height = 3300
        background = Image.new('RGBA', (background_width, background_height), (41, 41, 41, 255))
        assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        font = ImageFont.truetype(os.path.join(assets_path, 'SmileySans-Oblique.ttf'), 50)

        title_type = ['new_release', 'recent_update', 'today', 'weekly', 'monthly']
        title = Image.open(os.path.join(assets_path, f'{title_type[self.sort_by.value]}.png'))
        title_width = int(title.size[0] / title.size[1] * y_offset)
        title = title.resize((title_width, y_offset))

        for i in range(0, 10):
            img = Image.open(io.BytesIO(self.top_covers[i]))
            img = img.resize((800, 540), Image.LANCZOS)
            x = i % 2 * 800 + x_offset * (i % 2 + 1)
            y = i // 2 * 540 + y_offset * (i // 2 + 1)
            background.paste(img, (x, y))
            draw_id = ImageDraw.Draw(background)
            draw_id.text((x + 10, y + 550), self.top_ids[i], font=font, fill=(255, 153, 0))
            if i == 0:
                background.paste(title, ((background_width - title_width) // 2, 0), title)

        background.save(f'{self.movie_type.name}-{self.sort_by.name}-Top10.png')

    def download(self):
        self.save_path = os.path.join(self.base_save_path, self.sort_by.name)

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        for page in range(1, 2):
            videos = self.get_all_videos(page)

            for video in videos:
                movie_title = video.text.split('\n')[1]
                movie_id = video.get('alt')
                self.download_cover(movie_title, movie_id)

        self.show_top10()
