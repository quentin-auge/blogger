#!/usr/bin/env python

import abc
import logging
import os
from glob import glob

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


class TextExtractor:
    """
    Extract text from a HTML file.
    """

    def __init__(self, filepath):

        with open(filepath) as f:
            html = f.read()

        self.soup = BeautifulSoup(html, features='lxml')

    def get_html(self):
        return str(self.soup)

    def get_text(self):
        """
        Extract the text.
        """

        self.trim()

        text = self.soup.get_text()

        lines = []
        for line in text.splitlines():
            line = line.strip()
            if line:
                lines.append(line)

        text = ' '.join(lines).strip()

        return text

    @abc.abstractmethod
    def trim(self):
        """
        Trim page from non-text elements.
        """
        raise NotImplementedError

    def _remove_tags(self, tags):
        """
        Remove a list of tags from the page.
        """

        elts = self.soup.find_all(tags)
        for elt in elts:
            elt.decompose()

    def _remove_divs_by_class(self, classes):
        """
        Remove a list of divs identified by their class from the page.
        """

        classes = classes or []

        for div_class in classes:
            divs = self.soup.find_all('div', {'class': div_class})
            for div in divs:
                div.decompose()

    def _remove_divs_by_id(self, ids):
        """
        Remove a list of divs identified by their id from the page.
        """

        ids = ids or []

        for div_id in ids:
            divs = self.soup.find_all('div', {'id': div_id})
            for div in divs:
                div.decompose()


class BloggerTextExtractor(TextExtractor):
    """
    Extract text from blogger article.
    """

    def __init__(self, filepath):
        super().__init__(filepath)

    def trim(self):
        """
        Remove a list of common non-text tags from the page.
        """

        tags = ['script', 'style',
                'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'table', 'ul', 'dl']
        self._remove_tags(tags)

        classes = ['header section', 'widget PageList', 'blog-pager',
                   'sidebar section', 'post-footer', 'foot section',
                   'post-feeds']
        self._remove_divs_by_class(classes)


class WordpressTextExtractor(TextExtractor):
    """
    Extract text from wordpress article.
    """

    def __init__(self, filepath):
        super().__init__(filepath)

    def trim(self):
        tags = ['script', 'style',
                'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'table', 'ul', 'dl']
        self._remove_tags(tags)

        classes = ['ngg-galleryoverview', 'commentlist', 'navigation']
        self._remove_divs_by_class(classes)

        ids = ['respond', 'footer']
        self._remove_divs_by_id(ids)


def html_to_txt(html_folder, txt_folder, blog_name):
    """
    Extract the text from html articles. One txt file per html file.

    Args:
        html_folder (str): the source folder containing the raw HTML articles.
        txt_folder (str): the destination folder where extracted txt articles end up.
        blog_name (str): the blog to transform, either 'blogger' or 'wordpress'.
    """

    assert blog_name in ('blogger', 'wordpress'), f'invalid blog_name: {blog_name}'

    if blog_name == 'blogger':
        cls = BloggerTextExtractor
    elif blog_name == 'wordpress':
        cls = WordpressTextExtractor
    else:
        raise NotImplementedError

    html_filepaths = glob(os.path.join(html_folder, '*.html'))
    LOGGER.info(f'Processing {html_folder} ({len(html_filepaths)} articles)')

    for html_filepath in html_filepaths:
        text = cls(html_filepath).get_text()

        if not text:
            LOGGER.info(f'  Empty article {html_filepath}; skipping')
            continue

        html_filename = os.path.basename(html_filepath)
        txt_filename = html_filename.replace('html', 'txt')
        txt_filepath = os.path.join(txt_folder, txt_filename)
        LOGGER.info(f'  {html_filepath} -> {txt_filepath}')

        with open(txt_filepath, 'w') as f:
            f.write(text)


def normalize_txt(txt):
    """
    Convert some "exotic" characters to known ones.
    """

    # Non-breaking spaces -> regular spaces
    txt = txt.replace('\xa0', ' ')

    # Double quotes
    double_quotes_chars = '“”»«'
    for double_quotes_char in double_quotes_chars:
        txt = txt.replace(double_quotes_char, '"')

    # Single quotes
    single_quote_chars = '‘`´’'
    for single_quote_char in single_quote_chars:
        txt = txt.replace(single_quote_char, "'")

    # Triple dots
    txt = txt.replace('…', '...')

    # Hyphens
    hyphen_chars = '–—'
    for hyphen_char in hyphen_chars:
        txt = txt.replace(hyphen_char, '-')

    return txt


def restrict_to_vocab(txt, vocab):
    """
    Remove characters that do not belong the a vocabulary.
    """
    txt = ''.join(char for char in txt if char in vocab)
    return txt


def txt_to_one_txt(txt_folder, one_txt_filepath, vocab):
    """
    Restrict the set of characters used in txt articles and concatenate the result into one big
    txt file.

    Args:
        txt_folder (str): the source folder containing the txt articles.
        one_txt_filepath (str): the filepath to the output txt file.
        vocab (str): the set of characters to restrict the articles to.
    """

    filepaths = glob(os.path.join(txt_folder, '*.txt'))

    articles = []
    for filepath in filepaths:
        with open(filepath) as f:
            article = f.read()
            article = normalize_txt(article)
            article = restrict_to_vocab(article, vocab)
            articles.append(article)

    LOGGER.info(f'Writing {one_txt_filepath}')

    with open(one_txt_filepath, 'w') as f:
        f.write(' '.join(articles))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    blog_names = ('wordpress', 'blogger')

    # Raw HTML articles -> txt articles
    for blog_name in blog_names:
        html_to_txt(f'data/html/{blog_name}/', f'data/txt/{blog_name}/', blog_name)

    vocab = ' !"$%\'()+,-./0123456789:;=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    vocab += '_abcdefghijklmnopqrstuvwxyz~°àâçèéêëîïôùûœо€'

    # txt articles -> one clean txt
    for blog_name in blog_names:
        txt_to_one_txt(f'data/txt/{blog_name}/', f'data/one_txt/{blog_name}.txt', vocab)
