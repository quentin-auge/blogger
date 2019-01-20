## Datasets

The articles of two (french-speaking) travel blogs are downloaded: a blogger (blogspot) blog and a wordpress blog.

URLs are hidden purposefully in order to protect the identity of the downloaded blogs. As a consequence, you won't get full reproducibility here. Sorry.

The goal is to generate text that looks similar to the blogger blog. Since it is too small a dataset to learn from directly (77k words, 400k characters) we'll learn from a larger wordpress blog first (473k words, 2.7M characters).

Retrieving of the datasets is handled by two scripts:
 * [scrap_wordpress.py], which downloads the raw blogger HTML articles to `data/html/wordpress/`
 * [scrap_blogger.py], which downloads the raw wordpress HTML articles to `data/html/blogger/`
