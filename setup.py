from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='missav_toolbox',
    version='1.1.0',
    url='https://github.com/1bananachicken/MissAV-Toolbox',
    packages=find_packages(),
    install_requires=[
        'requests',
        'cloudscraper',
        'Pillow',
        'bs4',
        'm3u8',
        'natsort',
        'ffmpeg-python',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='bananachicken',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
