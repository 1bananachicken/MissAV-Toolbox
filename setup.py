from setuptools import setup, find_packages

setup(
    name='missav_utils',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'cloudscraper',
        'Pillow',
        'bs4',
    ],
    include_package_data=True,
    description='A brief description of my project',
    author='bananachicken',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
