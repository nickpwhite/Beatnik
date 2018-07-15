import itertools

from .Utils import Utils

class SearchHandler:
    def __init__(self, spotify_api, link_converter):
        self.spotify_api = spotify_api
        self.link_converter = link_converter

    def search(self, query):
        raw_results = self.spotify_api.search(query, limit=5, type="album,track")
        albums = raw_results.get('albums', {}).get('items', [])
        tracks = raw_results.get('tracks', []).get('items', [])

        ordered_results = [ result 
                for tup in itertools.zip_longest(albums, tracks) 
                for result in tup 
                if result is not None ]

        results = []

        for result in ordered_results:
            info = {
                'type': result['type'],
                'title': result['name'],
                'artist': result['artists'][0]['name'],
                'art': Utils.dict_find(result, 'images')[0]['url'],
                'album': result.get('album', {}).get('name'),
            }
            links = { 
                'apple_link': self.link_converter.get_apple_link(info),
                'gpm_link': self.link_converter.get_gpm_link(info),
                'soundcloud_link': self.link_converter.get_soundcloud_link(info),
                'spotify_link': result['external_urls']['spotify'] 
            }

            info['links'] = links

            results.append(info)

        return results
