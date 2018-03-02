import logging
import requests
import string
import urllib.parse as parse

from pyquery import PyQuery as pq

class SoundcloudApi:
    TRANS_TABLE = str.maketrans('', '', string.punctuation)

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.query_url = 'https://soundcloud.com/search?q={0}%20{1}'

    def get(self, url):
        d = pq(url=url)
        music_type = "album" if url.split('/')[4] == "sets" else "track"
        info = d("h1 > a")
        artwork = d("img").eq(1).attr("src")
        return {
            'type': music_type,
            'title': info.eq(0).html(),
            'artist': info.eq(1).html(),
            'art': artwork
        }

    def search(self, title, artist):
        query = self.query_url.format(title, artist).replace(' ', '%20')
        self.logger.info('query: {0}'.format(query))
        d = pq(url=query)
        
        expected_artist = artist.translate(self.TRANS_TABLE).lower()
        expected_title = title.translate(self.TRANS_TABLE).lower()
        results = d("ul:last > li > h2 > a")

        self.logger.info('exp_artist: {0}, exp_title: {1}'.format(expected_artist, expected_title))

        for item in results.items():
            text = item.text().lower()
            acutal_artist, actual_title, *other = text.split(' - ')
            actual_artist = acutal_artist.translate(self.TRANS_TABLE)
            actual_title = actual_title.translate(self.TRANS_TABLE)
            self.logger.info('artist: {0}, title: {1}'.format(actual_artist, actual_title))
            if expected_artist in actual_artist and expected_title in actual_title:
                href = 'https://soundcloud.com{0}'.format(item.attr.href)
                return href 

        return None
