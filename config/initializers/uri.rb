# frozen_string_literal: true
# typed: strict

module URI
  extend T::Sig

  @@hosts = T.let({}, T::Hash[String, T.untyped])

  class << self
    alias_method :parse_without_beatnik, :parse

    sig do
      params(
        uri: T.untyped
      )
      .returns(Generic)
    end
    def parse(uri)
      parsed = parse_without_beatnik(uri)
      host = parsed.host

      if host && (uri_class = @@hosts[host.downcase])
        uri_class.build(
          parsed.component.each_with_object({}) do |prop, hash|
            hash[prop] = parsed.public_send(prop)
          end
        ).tap {|new_uri| new_uri.scheme = parsed.scheme}
      else
        parsed
      end
    end
  end

  class AppleMusic < URI::HTTPS; end
  class Soundcloud < URI::HTTPS; end
  class Spotify < URI::HTTPS; end
  class Tidal < URI::HTTPS; end
  class YoutubeMusic < URI::HTTPS; end

  @@hosts['music.apple.com'] = AppleMusic
  @@hosts['soundcloud.com'] = Soundcloud
  @@hosts['open.spotify.com'] = Spotify
  @@hosts['tidal.com'] = Tidal
  @@hosts['music.youtube.com'] = YoutubeMusic
end
