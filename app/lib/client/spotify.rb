# frozen_string_literal: true
# typed: strict

module Client
  class Spotify < Base
    sig {override.params(music: Music).returns(Music)}
    def self.get_metadata(music)
      uri = URI.parse(music.spotify_url)
      path = path(uri)
      prefix, id = path.split('/')
      raise 'unable to get prefix or ID' if prefix.nil? || id.nil?

      if prefix == "album"
        result = RSpotify::Album.find(id)
        raise 'got multiple albums' if result.is_a?(Array)
        music.music_type = 'A'
      elsif prefix == "track"
        result = RSpotify::Track.find(id)
        raise 'got multiple tracks' if result.is_a?(Array)
        music.music_type = 'T'
        album = result.album
        if album.present?
          music.album = album.name
        end
      else
        raise 'unknown prefix'
      end

      artist_name = result.artists&.first&.name
      raise 'unable to get artist name' if artist_name.nil?

      music.name = result.name
      music.artist = artist_name

      music
    end

    sig {override.params(music: Music).returns(Music)}
    def self.get_url(music)
      return music if music.spotify_url.present?

      result = if music.music_type == 'A'
                 RSpotify::Album.search("#{music.name} #{music.artist}")
               elsif music.music_type == 'T'
                 RSpotify::Track.search("#{music.name} #{music.artist}")
               end&.first

      if result.present?
        music.spotify_url = result.external_urls["spotify"]
      end

      music
    end
  end
end
