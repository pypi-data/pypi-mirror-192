from setuptools import setup, find_packages

setup(
    name='zomato_scrape',
    version='1.0.0',
    author='Dinesh',
    author_email='dinudasari12@gmail.com',
    description='A package for scraping Zomato restaurant data',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'pandas',
        'selenium',
    ],
)