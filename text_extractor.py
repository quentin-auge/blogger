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

        text = ' '.join(lines)

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

        tags = ['script', 'style', 'title', 'h1', 'h2', 'h3', 'h4', 'table', 'ul']
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
        tags = ['script', 'style', 'title', 'h1', 'h2', 'h3', 'h4', 'table', 'ul', 'dl']
        self._remove_tags(tags)

        classes = ['ngg-galleryoverview', 'commentlist', 'navigation']
        self._remove_divs_by_class(classes)

        ids = ['respond', 'footer']
        self._remove_divs_by_id(ids)


if __name__ == '__main__':
    extractor = BloggerTextExtractor(glob('data/blogger/*')[0])
    #extractor = WordpressTextExtractor(glob('data/wordpress/*')[0])

    extractor.trim()

    with open('trimmed.html', 'w') as f:
        f.write(extractor.get_html())

    print(extractor.get_text())
