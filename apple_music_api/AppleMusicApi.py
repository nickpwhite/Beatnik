import datetime
import json
import jwt
import requests

class AppleMusicApi:
    def __init__(self, key_id, issuer, key_filename):
        key_file = open(key_filename, 'r')
        secret_key = key_file.read()
        key_file.close()
        iat = int(datetime.datetime.utcnow().strftime("%s"))
        exp = int((datetime.datetime.utcnow() + datetime.timedelta(hours=12)).strftime("%s"))
        algorithm = 'ES256'

        payload = {
            'iss': issuer,
            'iat': iat,
            'exp': exp
        }

        headers = {
            'alg': algorithm,
            'kid': key_id
        }

        token_bytes = jwt.encode(payload, secret_key, algorithm=algorithm, headers=headers)
        self.developer_token = token_bytes.decode()

    def _get(self, url, params={}):
        headers = { "Authorization": "Bearer {0}".format(self.developer_token) }
        response = requests.get(url, params=params, headers=headers)

        return json.loads(response.text)

    def get_album(self, album_id, storefront='us'):
        url = "https://api.music.apple.com/v1/catalog/{0}/albums/{1}".format(storefront, album_id)
        album = self._get(url)

        return album

    def get_track(self, track_id, storefront='us'):
        url = "https://api.music.apple.com/v1/catalog/{0}/songs/{1}".format(storefront, track_id)
        track = self._get(url)

        return track

    def search(self, term, limit=25, offset=0, types='artists, albums, songs, playlists, stations', storefront='us'):
        url = "https://api.music.apple.com/v1/catalog/{0}/search".format(storefront)
        params = {
            'term': term,
            'limit': limit,
            'offset': offset,
            'types': types
        }
        results = self._get(url, params)

        return results
