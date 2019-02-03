import os
from django.test import TestCase

from beatnik.api_manager.clients import AppleMusicApi

class TestAppleMusicApi(TestCase):

    def setUp(self):
        self.appleMusicApi = AppleMusicApi(os.environ['APPLE_KEY_ID'],
                os.environ['APPLE_KEY_ISSUER'],
                os.environ['APPLE_KEY'])

    def test_get_album(self):
        album_id = "1265893523"

        self.appleMusicApi.get_album(album_id)
