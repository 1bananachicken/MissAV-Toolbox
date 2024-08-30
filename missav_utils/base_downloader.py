import os


class BaseDownloader:
    def __init__(self, save_path='downloads'):
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        self.base_save_path = save_path
        self.save_path = None

        if os.environ.get('http_proxy') is not None and os.environ.get('https_proxy') is not None:
            self.proxy = {'http': os.environ.get('http_proxy'), 'https': os.environ.get('https_proxy')}
        else:
            self.proxy = None

    def __get_page_parser(self, *args, **kwargs):
        pass

    def __get_num_pages(self):
        pass

    def __get_links(self, *args, **kwargs):
        pass

    def __launch_download_process(self, *args, **kwargs):
        pass

    def download(self):
        pass

