import abc
import logging
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


def create_txt_dataset(blog_name):
    """
    Create txt dataset from html files.

    Args:
        blog_name (str): either 'blogger' or 'wordpress'.
    """

    assert blog_name in ('blogger', 'wordpress')

    if blog_name == 'blogger':
        cls = BloggerTextExtractor
    elif blog_name == 'wordpress':
        cls = WordpressTextExtractor
    else:
        raise NotImplementedError

    html_filepaths = glob(f'data/html/{blog_name}/*.html')
    LOGGER.info(f'processing {blog_name} ({len(html_filepaths)} articles)')

    for html_filepath in html_filepaths:
        text = cls(html_filepath).get_text()

        if not text:
            LOGGER.info(f'  Empty article {html_filepath}; skipping')
            continue

        txt_filepath = html_filepath.replace('html', 'txt')
        LOGGER.info(f'  {html_filepath} -> {txt_filepath}')

        with open(txt_filepath, 'w') as f:
            f.write(text)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # extractor = BloggerTextExtractor(glob('data/html/blogger/*')[0])
    # extractor = WordpressTextExtractor(glob('data/html/wordpress/*')[0])
    #
    # extractor.trim()
    #
    # with open('trimmed.html', 'w') as f:
    #     f.write(extractor.get_html())
    #
    # print(extractor.get_text())

    create_txt_dataset('blogger')
    create_txt_dataset('wordpress')
