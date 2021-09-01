# frozen_string_literal: true
# typed: strict

class AppleMusicAPI
  include Singleton

  sig {void}
  def initialize
    issuer = ENV['APPLE_KEY_ISSUER']
    iat = Time.now.to_i
    exp = 12.hours.from_now.to_i
    payload = {
      'iss': issuer,
      'iat': iat,
      'exp': exp,
    }

    key_id = ENV['APPLE_KEY_ID']
    headers = {
      'alg': 'ES256',
      'kid': key_id
    }
    secret_key = OpenSSL::PKey::EC.new(ENV['APPLE_KEY'])

    @developer_token = T.let(
      JWT.encode(payload, secret_key, 'ES256', headers),
      String,
    )
  end

  sig do
    params(
      path: String,
      query: T::Hash[Symbol, T.untyped]
    )
    .returns(
      T::Hash[String, T.untyped]
    )
  end
  private def _get(path, query={})
    response = Excon.get(
      "https://api.music.apple.com/v1/catalog/us/#{path}",
      query: query,
      headers: {"Authorization": "Bearer #{@developer_token}"},
    )

    JSON.parse(response.body)
  end

  sig {params(album_id: String).returns(T::Hash[String, T.untyped])}
  def get_album(album_id)
    response = _get("albums/#{album_id}")

    response["data"].first
  end

  sig {params(track_id: String).returns(T::Hash[String, T.untyped])}
  def get_track(track_id)
    response = _get("songs/#{track_id}")

    response["data"].first
  end

  sig do
    params(
      title: String,
      artist_name: String
    )
    .returns(
      T.nilable(T::Hash[String, T.untyped])
    )
  end
  def search_album(title, artist_name)
    params = {
      term: "#{title} #{artist_name}".delete(','),
      limit: 1,
      offset: 0,
      types: 'albums',
    }
    response = _get("search", params)
    results = response.dig("results", "albums", "data") || []

    results.first
  end

  sig do
    params(
      title: String,
      artist_name: String
    )
    .returns(
      T.nilable(T::Hash[String, T.untyped])
    )
  end
  def search_track(title, artist_name)
    params = {
      term: "#{title} #{artist_name}".delete(','),
      limit: 1,
      offset: 0,
      types: 'songs',
    }
    response = _get("search", params)
    results = response.dig("results", "songs", "data") || []

    results.first
  end
end
