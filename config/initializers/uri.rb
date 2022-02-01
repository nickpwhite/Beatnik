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
        args = parsed.component.each_with_object({}) do |prop, hash|
          hash[prop] = parsed.public_send(prop)
          if prop == :query && hash[prop].present?
            hash[prop] = Rack::Utils.build_query(Rack::Utils.parse_query(hash[prop]).compact)
          end
        end

        uri_class.build(args).tap {|new_uri| new_uri.scheme = parsed.scheme}
      else
        parsed
      end
    end
  end

  class Beatnik < URI::HTTPS; end
  class AppleMusic < Beatnik; end
  class Soundcloud < Beatnik; end
  class Spotify < Beatnik; end
  class Tidal < Beatnik; end
  class YoutubeMusic < Beatnik; end

  @@hosts['music.apple.com'] = AppleMusic
  @@hosts['soundcloud.com'] = Soundcloud
  @@hosts['open.spotify.com'] = Spotify
  @@hosts['tidal.com'] = Tidal
  @@hosts['music.youtube.com'] = YoutubeMusic
end
