from django.test import TestCase

from ..link_converter.LinkConverter import LinkConverter

class TestLinkConverter(TestCase):

    def setUp(self):
        self.linkConverter = LinkConverter()

    def test_get_gpm_album(self):
        album_info = {
            'type': "album",
            'title': "Skin",
            'artist': "Flume"
        }
        expected = "https://play.google.com/music/m/Bxzvlykr55sglkwvdm3sfchktxu"
        actual = self.linkConverter.get_gpm_album(album_info)
        self.assertEqual(expected, actual)

    def test_get_gpm_track(self):
        track_info = {
            'type': "track",
            'title': "Göd Grid",
            'artist': "Iglooghost"
        }
        expected = "https://play.google.com/music/m/Tdtnazb2qd2zkbu3zoagdq2aciu"
        actual = self.linkConverter.get_gpm_track(track_info)
        self.assertEqual(expected, actual)

    def test_get_spotify_album(self):
        album_info = {
            'type': "album",
            'title': "Venice",
            'artist': "Anderson .Paak"
        }
        expected = "https://open.spotify.com/album/2DOiha5oI19Dmw5M9ryHD8"
        actual = self.linkConverter.get_spotify_album(album_info)
        self.assertEqual(expected, actual)

    def test_get_spotify_track(self):
        track_info = {
            'type': "track",
            'title': "22 (OVER S∞∞N)",
            'artist': "Bon Iver"
        }
        expected = "https://open.spotify.com/track/5oK98mpTJSU0iqLHN1hZ3y"
        actual = self.linkConverter.get_spotify_track(track_info)
        self.assertEqual(expected, actual)
