from setuptools import setup, find_packages

setup(
    name='zomato',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'pandas',
        'selenium'
    ],
    entry_points={
        'console_scripts': [
            'zomato=scraper:main'
        ]
    },
    author='Dinesh',
    author_email='dinudasari12@gmail.com',
    description='Zomato restaurants Scraper',
)