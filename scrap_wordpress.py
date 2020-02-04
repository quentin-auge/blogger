#!/usr/bin/env python

import logging
import os
import re

import scrapy
import yaml
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.crawler import CrawlerProcess

LOGGER = logging.getLogger(__name__)


class WordpressSpider(scrapy.Spider):
    """
    Download articles from a wordpress blog.

    Start with the index page(s), and get all the articles listed there.
    """

    def __init__(self, articles_index_urls, dst_folder):
        super(WordpressSpider).__init__()
        self.start_urls = articles_index_urls
        self.dst_folder = dst_folder

    def parse(self, response):
        soup = BeautifulSoup(response.body, features='lxml')

        for a in soup.find_all('a'):
            href = a['href']
            if re.search(r'\?p=[0-9]+$', href):
                LOGGER.info(f'processing {a}')
                yield Request(href, self.save_article)

    def save_article(self, response):

        url = response.url
        html = response.body

        filename = url.split('/')[-1]
        # ?p=12345 -> 12345.html
        filename = filename[3:] + '.html'
        filepath = os.path.join(self.dst_folder, filename)

        LOGGER.info(f'Saving article to {filepath}')
        with open(filepath, 'wb') as f:
            f.write(html)


if __name__ == '__main__':
    # File `urls.yaml` is intentionally not committed in order to hide the identity
    # of the scraped blogs
    with open('urls.yaml') as f:
        urls = yaml.load(f.read())
        articles_index_urls = urls['wordpress']

    crawler = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'DOWNLOAD_DELAY': 3
    })
    crawler.crawl(WordpressSpider, articles_index_urls, dst_folder='data/html/wordpress/')
    crawler.start()
