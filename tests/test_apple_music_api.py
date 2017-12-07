import os
from django.test import TestCase

from ..apple_music_api.AppleMusicApi import AppleMusicApi

class TestAppleMusicApi(TestCase):

    def setUp(self):
        self.appleMusicApi = AppleMusicApi(key_id=os.environ['APPLE_KEY_ID'],
                issuer=os.environ['APPLE_KEY_ISSUER'],
                key_filename=os.environ['APPLE_KEY_PATH'])

    def test_get_album(self):
        album_id = "1265893523"

        self.appleMusicApi.get_album(album_id)
