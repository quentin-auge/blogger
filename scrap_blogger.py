#!/usr/bin/env python

import logging
import os

import scrapy
import yaml
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.crawler import CrawlerProcess

LOGGER = logging.getLogger(__name__)


class BloggerSpider(scrapy.Spider):
    """
    Scrap blogger articles.

    Start with an article, and proceed to the previous article repeatedly
    until there is not article left.
    """

    def __init__(self, start_article_url):
        super(BloggerSpider).__init__()
        self.start_urls = [start_article_url]
        self.folder = 'data/html/blogger/'

    def parse(self, response):
        url = response.url
        html = response.body
        self.save_article(url, html)
        yield from self.fetch_previous_article(html)

    def fetch_previous_article(self, html):
        soup = BeautifulSoup(html, features='lxml')

        for a in soup.find_all('a', {'class': 'blog-pager-older-link'}):
            yield Request(a['href'], self.parse)

    def save_article(self, url, html):
        filename = url.split('/')[-1]
        filepath = os.path.join(self.folder, filename)

        LOGGER.info(f'Saving article to {filepath}')
        with open(filepath, 'wb') as f:
            f.write(html)


if __name__ == '__main__':
    # File `urls.yaml` is intentionally not committed in order to hide the identity
    # of the scraped blogs
    with open('urls.yaml') as f:
        urls = yaml.load(f.read())
        start_article_url = urls['blogger']

    crawler = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                              'DOWNLOAD_DELAY': 3})
    crawler.crawl(BloggerSpider, start_article_url)
    crawler.start()
