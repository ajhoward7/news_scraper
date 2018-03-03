import requests
from bs4 import BeautifulSoup
import sys
import json

import lib


def fetch_tag_safe(item,tag):
    """
    For an item, return value associated with a particular tag - avoiding an error if not present
    """
    try:
        return getattr(getattr(item,tag),"text")
    except:
        # Do something
        pass

def fetch_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    articles = soup.find_all("item")
    return articles


if __name__ == "__main__":
    rss_feeds = lib.get_conf("rss_feeds", path = 'conf/confs.rss.yaml')

    output_dict = {}
    try:
        output_filename = sys.argv[1]
    except:
        output_filename = 'output.json'

    for url in rss_feeds:
        articles = fetch_articles(url)

        output_articles = []
        for article in articles:
            article_output = {}
            article_output['title'] = fetch_tag_safe(article,"title")
            article_output['description'] = fetch_tag_safe(article, "description")
            article_output['link'] = fetch_tag_safe(article, "link")
            article_output['pubDate'] = fetch_tag_safe(article, "pubDate")
            article_output['source'] = fetch_tag_safe(article, "source")

            # Can add more tags here

            output_articles.append(article_output)

        output_dict[url] = output_articles

    f = open(output_filename, 'w')
    json.dump(output_dict,f)
    f.close()

    print "Completed Analysis, output is in {}".format(output_filename)

