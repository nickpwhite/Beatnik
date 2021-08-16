# frozen_string_literal: true
# typed: strict

class MusicController < ApplicationController
  class ShowParams < T::Struct
    const :id, Integer
  end

  class CreateParams < T::Struct
    const :query, String
  end

  sig {void}
  def show
    typed_params = TypedParams[ShowParams].new.extract!(params)

    music = Music.find(typed_params.id)

    render :show, locals: {music: music}
  end

  sig {void}
  def create
    typed_params = TypedParams[CreateParams].new.extract!(params)
    uri = URI.parse(typed_params.query)

    if !(uri.class < URI::HTTP)
      search_results = SearchClient.instance.search(typed_params.query)
      render :search_results, locals: {search_results: search_results}
      return
    end

    music =
      case uri
      when URI::AppleMusic
        Music.find_or_create_by(apple_url: uri.to_s)
      when URI::Soundcloud
        Music.find_or_create_by(soundcloud_url: uri.to_s)
      when URI::Spotify
        Music.find_or_create_by(spotify_url: uri.to_s)
      when URI::Tidal
        Music.find_or_create_by(tidal_url: uri.to_s)
      when URI::YoutubeMusic
        Music.find_or_create_by(ytm_url: uri.to_s)
      else
        render status: :bad_request
        return
      end

    if music.nil?
      render status: :not_found
      return
    end

    redirect_to music
  end
end
