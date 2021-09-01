# frozen_string_literal: true
# typed: strict

module TidalAPI
  class Client
    include Singleton

    sig {void}
    def initialize
      @client_id = T.let(ENV.fetch('TIDAL_CLIENT_ID'), String)
      @session_id = T.let(ENV.fetch('TIDAL_SESSION_ID'), String)
      @access_token = T.let(ENV.fetch('TIDAL_ACCESS_TOKEN'), String)
      @token_type = T.let(ENV.fetch('TIDAL_TOKEN_TYPE'), String)
      @refresh_token = T.let(ENV.fetch('TIDAL_REFRESH_TOKEN'), String)

      response = _get("sessions")
      body = JSON.parse(response.body)
      # subStatus 11003 corresponds to a token that has "expired on time"
      if response.status == 401 && body.fetch("subStatus") == 11003
        refresh_response = _post(
          "https://auth.tidal.com/v1/oauth2/token",
          {
            grant_type: 'refresh_token',
            refresh_token: @refresh_token,
            client_id: @client_id,
            client_secret: @client_id,
          }
        )

        body = JSON.parse(refresh_response.body)
        @access_token = body["access_token"]
      end
    end

    sig {params(album_id: String).returns(T::Hash[String, T.untyped])}
    def get_album(album_id)
      response = _get("albums/#{album_id}")

      JSON.parse(response.body)
    end

    sig {params(track_id: String).returns(T::Hash[String, T.untyped])}
    def get_track(track_id)
      response = _get("tracks/#{track_id}")

      JSON.parse(response.body)
    end

    sig do
      params(
        query: String,
        type: String
      )
      .returns(
        T::Hash[String, T.untyped]
      )
    end
    def search(query, type)
      response = _get("search/#{type}", {query: query})

      JSON.parse(response.body)
    end

    sig {params(path: String, query: T::Hash[Symbol, T.untyped]).returns(Excon::Response)}
    private def _get(path, query={})
      Excon.get(
        "https://api.tidalhifi.com/v1/#{path}",
        query: {
          sessionId: @session_id,
          countryCode: "US",
          limit: "999"
        }.merge(query),
        headers: {authorization: "#{@token_type} #{@access_token}"},
      )
    end

    sig do
      params(
        url: String,
        params: T::Hash[Symbol, String]
      )
      .returns(T.untyped)
    end
    private def _post(url, params)
      Excon.post(
        url,
        query: URI.encode_www_form(params),
        headers: {"Content-Type" => "application/x-www-form-urlencoded"},
      )
    end
  end
end
