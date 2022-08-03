# frozen_string_literal: true
# typed: strict

module Client
  class Spotify < Base
    sig {override.params(music: Music).returns(Music)}
    def self.get_metadata(music)
      uri = URI.parse(music.spotify_url)
      path = path(uri)
      _, prefix, id = path.split('/')
      raise 'unable to get prefix or ID' if prefix.nil? || id.nil?

      authenticate
      if prefix == "album"
        result = RSpotify::Album.find(id)
        raise 'got multiple albums' if result.is_a?(Array)
        music.music_type = 'A'
        music.artwork = find_artwork(result.images)
      elsif prefix == "track"
        result = RSpotify::Track.find(id)
        raise 'got multiple tracks' if result.is_a?(Array)
        music.music_type = 'T'
        album = result.album
        if album.present?
          music.album = album.name
          music.artwork = find_artwork(album.images)
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

      authenticate
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

    sig {params(query: String).returns(T::Array[T::Hash[Symbol, T.nilable(String)]])}
    def self.search(query)
      return [] if query.blank?

      authenticate
      # The Spotify client modifies the types string, calling #dup here unfreezes it.
      types = 'album,track'.dup
      results = RSpotify::Base.search(query, types, limit: 5)
      results.filter_map do |album_or_track|
        url = album_or_track.external_urls['spotify']
        next if url.blank?

        artwork = if album_or_track.is_a?(RSpotify::Album)
          find_artwork(album_or_track.images)
        else
          find_artwork(album_or_track.album&.images)
        end
        next if artwork.blank?

        result = {
          name: album_or_track.name,
          artist: album_or_track.artists.first&.name,
          url: url,
          artwork: artwork,
        }

        result
      end
    end

    sig {params(music: Music).returns(T.nilable(String))}
    def self.get_artwork(music)
      uri = URI.parse(music.spotify_url)
      path = path(uri)
      _, prefix, id = path.split('/')
      return if prefix.nil? || id.nil?

      authenticate
      if prefix == "album"
        result = RSpotify::Album.find(id)
      elsif prefix == "track"
        result = RSpotify::Track.find(id)
      end

      find_artwork(result.images)
    end

    sig {void}
    def self.authenticate
      RSpotify.authenticate(ENV['SPOTIFY_CLIENT_ID'], ENV['SPOTIFY_CLIENT_SECRET'])
    end

    sig {params(images: T::Array[T::Hash[String, T.untyped]]).returns(T.nilable(String))}
    def self.find_artwork(images)
      image = (images.find {|i| i["height"] == i["weight"]} || images.first)
      image && image["url"]
    end
    private_class_method :authenticate, :find_artwork
  end
end
