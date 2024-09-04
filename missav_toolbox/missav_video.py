import os
import m3u8
import ffmpeg
import requests.exceptions
import multiprocessing as mp
from natsort import natsorted
from missav_toolbox.type_enum import MovieType, SortBy
from missav_toolbox.base_downloader import BaseDownloader


class VideoDownloader(BaseDownloader):
    def __init__(self, save_path='videos', movie_type=MovieType.professional, sort_by=SortBy.ReleaseDate,
                 keywords=None):
        super().__init__(save_path, movie_type, sort_by, keywords)

        self.video_id = None

    def download_segment(self, base_link, suffix, segment):
        video_link = base_link + '/' + suffix.split('/')[0] + '/' + segment
        video = self.get_scraper().get(video_link, proxies=self.proxy, headers=self.headers)

        segment = segment.replace('jpeg', 'ts')
        segment_save_path = os.path.join(self.save_path, segment)

        if os.path.exists(segment_save_path):
            return

        print(f'Downloading {segment}')
        with open(segment_save_path, 'wb') as f:
            f.write(video.content)

    def download_video(self, link):
        page_parser = self.get_page_parser(link)
        js = page_parser.find_all('script', type='text/javascript')

        index_begin = js[2].text.find('m3u8')
        index_offset = 112
        uuid = js[2].text[index_begin: index_begin + index_offset].split('|')
        base_link = 'https://surrit.com/' + '-'.join(uuid[i] for i in range(5, 0, -1))

        try:
            m3u8_playlist_content = self.scraper.get(base_link + '/playlist.m3u8', proxies=self.proxy,
                                                     headers=self.headers)
            m3u8_playlist_content.raise_for_status()
        except requests.exceptions.HTTPError:
            raise requests.HTTPError('Can\'t fetch the content')

        m3u8_playlist = m3u8.loads(m3u8_playlist_content.text)
        suffix = m3u8_playlist.playlists[-1].uri

        try:
            m3u8_video_content = self.scraper.get(base_link + '/' + suffix, proxies=self.proxy, headers=self.headers)
            m3u8_video_content.raise_for_status()
        except requests.exceptions.HTTPError:
            raise requests.HTTPError('Can\'t fetch the content')

        m3u8_video = m3u8.loads(m3u8_video_content.text)
        segments = m3u8_video.segments.uri

        pool = mp.Pool(mp.cpu_count())
        for segment in segments:
            pool.apply_async(self.download_segment, args=(base_link, suffix, segment))
        pool.close()
        pool.join()

        # for segment in segments:
        #     self.download_segment(base_link, suffix, segment)

    def merge_video(self):
        video_output_path = os.path.join(self.save_path, f'{self.video_id}.mp4')
        if os.path.exists(video_output_path):
            return

        video_files = os.listdir(self.save_path)
        video_files = natsorted(video_files)
        video_list_path = os.path.join(self.save_path, 'file_list.txt')

        with open(os.path.join(self.save_path, 'file_list.txt'), 'w') as f:
            for video_file in video_files:
                if video_file == 'file_list.txt':
                    continue
                f.write(f'file {video_file}\n')

        ffmpeg.input(video_list_path, format='concat', safe=0).output(video_output_path, c='copy').run()

    def delete_cache(self):
        caches = os.listdir(self.save_path)
        for cache in caches:
            if cache.endswith('.ts') or cache.endswith('.txt'):
                os.remove(os.path.join(self.save_path, cache))

    def download(self):
        video = self.get_all_videos()[0]
        self.video_id = video.get('alt')
        self.save_path = os.path.join(self.base_save_path, self.video_id)
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        link = video['href']
        self.download_video(link)
        self.merge_video()
        self.delete_cache()
