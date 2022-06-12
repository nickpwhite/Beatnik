# frozen_string_literal: true
# typed: strict

class Music < ApplicationRecord
  PAGE_SIZE = 10

  self.table_name = "beatnik_music"

  # Default model attributes
  attribute :album, :string, default: ""
  attribute :match_rating, :integer, default: 0

  typed_enum source: {
    AppleMusic: "apple_music",
    Soundcloud: "soundcloud",
    Spotify: "spotify",
    Tidal: "tidal",
    YoutubeMusic: "youtube_music",
  }

  sig {returns(ActiveRecord::Relation)}
  def self.for_feed
    where.not(artwork: '').order(id: :desc)
  end

  sig {params(page: Integer).returns(ActiveRecord::Relation)}
  def self.get_feed(page)
    for_feed.limit(PAGE_SIZE).offset(page * PAGE_SIZE)
  end

  sig {params(uri: URI::HTTP, blk: T.proc.returns(T.nilable(Music))).returns(T.nilable(Music))}
  def self.from_uri(uri, blk)
    case uri
    when URI::AppleMusic
      Music.find_or_initialize_by(apple_url: uri.to_s) do |music|
        music.typed_source = Music::Source::AppleMusic
      end
    when URI::Soundcloud
      Music.find_or_initialize_by(soundcloud_url: uri.to_s) do |music|
        music.typed_source = Music::Source::Soundcloud
      end
    when URI::Spotify
      Music.find_or_initialize_by(spotify_url: uri.to_s) do |music|
        music.typed_source = Music::Source::Spotify
      end
    when URI::Tidal
      Music.find_or_initialize_by(tidal_url: uri.to_s) do |music|
        music.typed_source = Music::Source::Tidal
      end
    when URI::YoutubeMusic
      uri.query = Rack::Utils.build_query(Rack::Utils.parse_query(uri.query).without("feature"))
      Music.find_or_initialize_by(ytm_url: uri.to_s) do |music|
        music.typed_source = Music::Source::YoutubeMusic
      end
    else
      if block_given?
        yield
      else
        nil
      end
    end
  end

  sig {returns(String)}
  def humanized_type
    case music_type
    when "T"
      "track"
    when "A"
      "album"
    else
      raise "Unknown music type #{music_type}"
    end
  end
end
