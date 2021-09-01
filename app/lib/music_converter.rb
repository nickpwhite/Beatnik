# frozen_string_literal: true
# typed: ignore

class MusicConverter
  sig {params(music: Music).void}
  def initialize(music)
    @music = music
  end

  sig {returns(Music)}
  def convert
    populate_metadata
    populate_urls

    @music
  end

  sig {void}
  private def populate_metadata
    @music =
      case @music.typed_source
      when Music::Source::AppleMusic
        Client::AppleMusic.get_metadata(@music)
      when Music::Source::Soundcloud
        Client::Soundcloud.get_metadata(@music)
      when Music::Source::Spotify
        Client::Spotify.get_metadata(@music)
      when Music::Source::Tidal
        Client::Tidal.get_metadata(@music)
      when Music::Source::YoutubeMusic
        Client::YoutubeMusic.get_metadata(@music)
      end
  end

  sig {void}
  private def populate_urls
    @music = Client::AppleMusic.get_url(@music)
    @music = Client::Soundcloud.get_url(@music)
    @music = Client::Spotify.get_url(@music)
    @music = Client::Tidal.get_url(@music)
    @music = Client::YoutubeMusic.get_url(@music)
  end
end
