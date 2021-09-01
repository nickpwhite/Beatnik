# frozen_string_literal: true
# typed: strict

require 'tidal_api'

module Client
  class Tidal < Base
    sig {override.params(music: Music).returns(Music)}
    def self.get_metadata(music)
      uri = URI.parse(music.tidal_url)
      path = path(uri)

      if uri.host == "listen.tidal.com"
        _, type, id = path.split("/")
      else
        _, _, type, id = path.split("/")
      end
      raise 'unable to get type or ID' if type.nil? || id.nil?

      if type == "album"
        result = TidalAPI::Client.instance.get_album(id)
        music.music_type = 'A'
        artwork_path = result["cover"].gsub("-", "/")
      elsif type == "track"
        result = TidalAPI::Client.instance.get_track(id)
        music.music_type = 'T'
        music.album = result.dig("album", "title")
        artwork_path = result.dig("album", "cover").gsub("-", "/")
      else
        raise "unknown type #{type}"
      end

      music.name = result["title"]
      music.artist = result.dig("artist", "name")
      music.artwork =
        "https://resources.tidal.com/images/#{artwork_path}/1280x1280.jpg"

      music
    end

    sig {override.params(music: Music).returns(Music)}
    def self.get_url(music)
      return music if music.tidal_url.present?

      result = if music.music_type == 'A'
                 TidalAPI::Client.instance
                   .search("#{music.name} #{music.artist}", "albums")
               elsif music.music_type == 'T'
                 TidalAPI::Client.instance
                   .search("#{music.name} #{music.artist}", "tracks")
               end

      if result.present?
        music.tidal_url = result.dig("items", 0, "url")
      end

      music
    end
  end
end
