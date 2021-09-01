# frozen_string_literal: true
# typed: ignore

require 'apple_music_api'

module Client
  class AppleMusic < Base
    sig {override.params(music: Music).returns(Music)}
    def self.get_metadata(music)
      uri = URI.parse(music.apple_url)

      if uri.query.blank?
        path = path(uri)
        album_id = path.split('/').last
        raise 'unable to get album ID' if album_id.nil?
        result = AppleMusicAPI.instance.get_album(album_id)
        music.music_type = 'A'
      else
        track_id = Rack::Utils.parse_nested_query(uri.query)['i']
        result = AppleMusicAPI.instance.get_track(track_id)
        music.music_type = 'T'
        music.album = result['attributes']['albumName']
      end

      art = result['attributes']['artwork']

      music.name = result['attributes']['name']
      music.artist = result['attributes']['artistName']
      music.artwork = art['url']
        .gsub("{w}", art['width'].to_s)
        .gsub("{h}", art['height'].to_s)

      music
    end

    sig {override.params(music: Music).returns(Music)}
    def self.get_url(music)
      return music if music.apple_url.present?

      result = if music.music_type == 'A'
                 AppleMusicAPI.instance.search_album(music.name, music.artist)
               elsif music.music_type == 'T'
                 AppleMusicAPI.instance.search_track(music.name, music.artist)
               end

      if result.present?
        music.apple_url = result.dig('attributes', 'url')
      end

      music
    end
  end
end
