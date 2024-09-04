from setuptools import setup, find_packages

setup(
    name='missav_toolbox',
    version='1.0.0',
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
    include_package_data=True,
    author='bananachicken',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache-2.0 License',
        'Operating System :: OS Independent',
    ],
)
