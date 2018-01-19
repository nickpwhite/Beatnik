import requests
import urllib.parse as parse

from pyquery import PyQuery as pq

class SoundcloudApi:
    def __init__(self):
        self.query_url = 'https://www.google.com/search?q=site%3Asoundcloud.com+{0}+{1}'

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
        d = pq(url=self.query_url.format(title, artist).replace(' ', '+'))

        expected_text = "{0} by {1}".format(title, artist).lower()
        
        results = d("h3.r > a")

        for item in results.items():
            text = item.html().replace('<b>', '').replace('</b>', '').split(' | F')[0].lower()
            if (text == expected_text):
                parsed_href = parse.urlparse(item.attr.href)
                url = parse.parse_qs(parsed_href.query)['q'][0]
                return url

        return None
