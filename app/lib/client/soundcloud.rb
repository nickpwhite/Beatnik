# frozen_string_literal: true
# typed: strict

require 'soundcloud_api'

module Client
  class Soundcloud < Base
    sig {override.params(music: Music).returns(Music)}
    def self.get_metadata(music)
      uri = URI.parse(music.soundcloud_url)
      _artist_slug, track_slug, set_slug = path(uri).split('/')

      if track_slug == "sets" && set_slug.nil?
        result = SoundcloudAPI::Client.instance.get_album(uri.to_s)
        music.music_type = 'A'
      else
        result = SoundcloudAPI::Client.instance.get_track(uri.to_s)
        music.music_type = 'T'
        music.album = result['album']
      end

      music.name = result['name']
      music.artist = result['artist']
      music.artwork = result['artwork']

      music
    end

    sig {override.params(music: Music).returns(Music)}
    def self.get_url(music)
      return music if music.soundcloud_url.present?

      result = if music.music_type == 'A'
                 SoundcloudAPI::Client.instance
                   .search_album(music.name, music.artist)
               elsif music.music_type == 'T'
                 SoundcloudAPI::Client.instance
                   .search_track(music.name, music.artist)
               end

      if result.present?
        music.soundcloud_url = result
      end

      music
    end
  end
end

