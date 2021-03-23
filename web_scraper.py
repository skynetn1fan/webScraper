"""
Create a webscraper based on the udemy course ZTM
"""

import sys
import requests
from bs4 import BeautifulSoup
import pprint
import os

path = sys.argv[1]
parser = 'html.parser'
topics = list(sys.argv[3:])
res = requests.get(path)
soup = BeautifulSoup(res.text, parser)

# We want to select all posts that have a score > 100
links = soup.select('.storylink')
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['Votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points >= 100:
            # if any(x in title for x in topics):
                hn.append({"title": title, "href": href, "Votes": points})

    return hn

def select_multiple_pages(pages, path):
    for i in range(pages):
        res = requests.get(path + f"?p={i}")
        soup = BeautifulSoup(res.text, parser)
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        pprint.pprint(sort_stories_by_votes(create_custom_hn(links, subtext)))

select_multiple_pages(4, path)