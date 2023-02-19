# frozen_string_literal: true
# typed: strict

class Settings < ApplicationRecord
  typed_enum redirect: {
    None: "none",
    AppleMusic: "apple_music",
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

    sig {params(music: Music).returns(T.nilable(String))}
    def music_url(music)
      case self
      when None
        nil
      when AppleMusic
        music.apple_url
      when Spotify
        music.spotify_url
      when Tidal
        music.tidal_url
      when YoutubeMusic
        music.ytm_url
      else
        T.absurd(self)
      end
    end
  end
end
