# frozen_string_literal: true
# typed: strict

module YoutubeMusicAPI
  class Client
    include Singleton

    sig {params(album_id: String).returns(T::Hash[String, String])}
    def get_album(album_id)
      response = _get("https://music.youtube.com/playlist", {list: album_id})
      browse_id = /"(MPRE[^"\\]*)\\"/.match(response.body) {|match| match[1]}
      raise 'unable to find browse_id' if browse_id.nil?

      album_response = _post(
        url("browse"),
        {
          browseEndpointContextSupportedConfigs: {
            browseEndpointContextMusicConfig: {
              pageType: "MUSIC_PAGE_TYPE_ALBUM"
            }
          },
          browseId: browse_id,
          context: {
            client: {
              clientName: "WEB_REMIX",
              clientVersion: "0.1",
              hl: "en"
            },
            user: {}
          }
        }
      )

      album_info = JSON.parse(album_response.body)
        .dig("header", "musicDetailHeaderRenderer")

      {
        "name" => album_info.dig("title", "runs", 0, "text"),
        "artist" => album_info.dig("subtitle", "runs", 2, "text"),
        "artwork" => get_artwork(album_info.dig(
          "thumbnail", "croppedSquareThumbnailRenderer", "thumbnail", "thumbnails"
        ))
      }
    end

    sig {params(track_id: String).returns(T::Hash[String, T.untyped])}
    def get_track(track_id)
      response = _post(
        url("player"),
        {
          contentPlaybackContext: {
            signatureTimestamp: Time.now.to_i / 60 / 60 / 24,
          },
          video_id: track_id,
          context: {
            client: {
              clientName: "WEB_REMIX",
              clientVersion: "0.1",
              hl: "en"
            },
            user: {}
          }
        }
      )

      track_info = JSON.parse(response.body)["videoDetails"]

      {
        "name" => track_info["title"],
        "artist" => track_info["author"],
        "artwork" => get_artwork(track_info.dig("thumbnail", "thumbnails")),
      }
    end

    sig {params(query: String, type: T.nilable(String)).returns(T.nilable(String))}
    def search(query, type)
      response = _post(
        url("search"),
        {
          query: query,
          context: {
            client: {
              clientName: "WEB_REMIX",
              clientVersion: "0.1",
              hl: "en"
            },
            user: {}
          }
        }
      )
      body = JSON.parse(response.body)

      if type == "album"
        id = body.deep_find("playlistId")
        "https://music.youtube.com/playlist?list=#{id}"
      elsif type == "track"
        id = body.deep_find("videoId")
        "https://music.youtube.com/watch?v=#{id}"
      end
    end

    sig do
      params(
        url: String,
        params: T::Hash[Symbol, String]
      )
      .returns(Excon::Response)
    end
    private def _get(url, params)
      Excon.get(
        url,
        query: params,
        headers: {
          "user-agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        }
      )
    end

    sig do
      params(
        url: String,
        params: T::Hash[String, T.untyped],
      )
      .returns(Excon::Response)
    end
    private def _post(url, params)
      Excon.post(
        url,
        body: JSON.dump(params),
        headers: {
          'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
          'accept' => '*/*',
          'Connection' => 'keep-alive',
          'content-type' => 'application/json',
          'content-encoding' => 'gzip',
          'origin' => 'https://music.youtube.com',
          'x-goog-authuser' => '0',
          'X-Goog-Visitor-Id' => visitor_id,
        }
      )
    end

    sig {params(path: String).returns(String)}
    private def url(path)
      "https://www.youtube.com/youtubei/v1/#{path}"\
        "?alt=json&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
    end

    sig {returns(T.nilable(String))}
    private def visitor_id
      return @visitor_id if defined?(@visitor_id)

      response = _get('https://music.youtube.com', {})
      config = response.body.match(/ytcfg\.set\(({.+})\);/)

      if config
        @visitor_id = T.let(
          JSON.parse(config[1])['VISITOR_DATA'], T.nilable(String)
        )
      end
    end

    sig do
      params(
        thumbnails: T::Array[T::Hash[String, T.untyped]]
      )
      .returns(T.nilable(String))
    end
    private def get_artwork(thumbnails)
      if (thumbnail = thumbnails.max_by {|t| t["width"] + t["height"]})
        thumbnail["url"]
      end
    end
  end
end
