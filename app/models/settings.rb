# frozen_string_literal: true
# typed: strict

class Settings < ApplicationRecord
  typed_enum redirect: {
    None: "none",
    AppleMusic: "apple_music",
    Soundcloud: "soundcloud",
    Spotify: "spotify",
    Tidal: "tidal",
    YoutubeMusic: "youtube_music",
  }

  validates :visitor_id, :redirect, presence: true

  class Redirect < T::Enum
    sig {returns(String)}
    def humanize
      case self
      when None
        "None"
      when AppleMusic
        "Apple Music"
      when Soundcloud
        "Soundcloud"
      when Spotify
        "Spotify"
      when Tidal
        "Tidal"
      when YoutubeMusic
        "Youtube Music"
      else
        T.absurd(self)
      end
    end
  end
end
