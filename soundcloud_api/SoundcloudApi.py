import logging
import requests
import string
import urllib.parse as parse

from pyquery import PyQuery as pq

class SoundcloudApi:
    TRANS_TABLE = str.maketrans('', '', string.punctuation)

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.query_url = 'https://soundcloud.com/search?q={0}+{1}'

    def get(self, url):
        d = pq(url=url)
        music_type = "album" if url.split('/')[4] == "sets" else "track"
        info = d("h1 > a")
        title = info.eq(0).html()
        artist = info.eq(1).html()
        artwork = d("img").eq(1).attr("src")
        self.logger.info('title: {0} artist: {1}'.format(title, artist))
        return {
            'type': music_type,
            'title': info.eq(0).html(),
            'artist': info.eq(1).html(),
            'art': artwork
        }

    def search(self, title, artist):
        clean_title = title.replace(' & ', '+')
        clean_artist = artist.replace(' & ', '+')
        query = self.query_url.format(clean_title, clean_artist).replace(' ', '+')
        self.logger.info('query: {0}'.format(query))
        d = pq(url=query)
        
        expected_artist = clean_artist.lower()
        expected_title = clean_title.lower()
        results = d("ul:last > li > h2 > a")

        for item in results.items():
            text = item.text().lower()
            self.logger.info('text: {0}'.format(text))
            self.logger.info('title: {0}'.format(title))
            if title.lower() in text:
                href = 'https://soundcloud.com{0}'.format(item.attr.href)
                return href 

        return None
