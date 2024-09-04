from setuptools import setup, find_packages

setup(
    name='missav_toolbox',
    version='0.2.1',
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
    include_package_data=True,
    author='bananachicken',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
