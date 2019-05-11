import itertools

from beatnik.api_manager.utils import Utils

class SearchHandler:
    def __init__(self, spotify_api, link_converter):
        self.spotify_api = spotify_api
        self.link_converter = link_converter

    def search(self, query):
        raw_results = self.spotify_api.search(query, limit=5, type="album,track")
        albums = raw_results.get('albums', {}).get('items', [])
        tracks = raw_results.get('tracks', []).get('items', [])

        return [
            self.get_info(result)
            for tup in itertools.zip_longest(albums, tracks)
            for result in tup
            if result is not None
            if result.get('external_urls', {}).get('spotify') is not None
        ]

    def get_info(self, result):
        link = result.get('external_urls', {}).get('spotify')

        return {
            'name': result['name'],
            'artist': result['artists'][0]['name'],
            'album': result.get('album', {}).get('name'),
            'artwork': Utils.dict_find(result, 'images')[0]['url'],
            'url': f'/search?q={link}'
        }
