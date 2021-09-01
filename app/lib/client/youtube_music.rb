# frozen_string_literal: true
# typed: ignore

require 'youtube_music_api'

module Client
  class YoutubeMusic < Base
    sig {override.params(music: Music).returns(Music)}
    def self.get_metadata(music)
      uri = URI.parse(music.ytm_url)
      prefix, _ = path(uri)

      if prefix == "/playlist"
        album_id = Rack::Utils.parse_nested_query(uri.query)['list']
        result = YoutubeMusicAPI::Client.instance.get_album(album_id)
        music.music_type = 'A'
      elsif prefix == "/watch"
        track_id = Rack::Utils.parse_nested_query(uri.query)['v']
        result = YoutubeMusicAPI::Client.instance.get_track(track_id)
        music.music_type = 'T'
        music.album = ''
      else
        raise "unknown prefix #{prefix}"
      end

      music.name = result['name']
      music.artist = result['artist']
      music.artwork = result['artwork']

      music
    end

    sig {override.params(music: Music).returns(Music)}
    def self.get_url(music)
      return music if music.ytm_url.present?

      type = if music.music_type == 'A'
               "album"
             elsif music.music_type == 'T'
               "track"
             end

      result = YoutubeMusicAPI::Client.instance
        .search("#{music.name} #{music.artist}", type)

      if result.present?
        music.ytm_url = result
      end

      music
    end
  end
end
