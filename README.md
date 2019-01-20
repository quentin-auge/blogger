## Data

The articles of two (french-speaking) travel blogs are downloaded: a blogger (blogspot) blog and a wordpress blog.

*Note*: URLs are hidden purposefully in order to protect the identity of the downloaded blogs. You won't be able to access the data. Sorry.

The goal is to generate text that looks similar to the blogger blog. Since it is too small a dataset to learn from directly (77k words, 400k characters) we'll learn from a larger wordpress blog first (473k words, 2.7M characters).

Retrieving and cleaning the datasets is handled by three scripts:
  * [scrap_wordpress.py] downloads the raw blogger HTML articles.
  * [scrap_blogger.py] downloads the raw wordpress HTML articles.
  * [html_to_txt.py] transforms the raw HTML articles to txt articles. It further discards non-relevant characters (see [analyze_vocab.ipynb]) and concatenates the result into one txt file.
