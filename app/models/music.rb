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
