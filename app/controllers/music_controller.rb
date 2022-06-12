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
    settings = Settings.find_by(visitor_id: session[:visitor_id])
    if (redirect_url = settings&.typed_redirect&.music_url(music))
      redirect_to redirect_url
    else
      render :show, locals: {music: music}
    end
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

    music = Music.from_uri(uri) do
      render status: :bad_request
      return
    end

    if music.nil?
      render status: :not_found
      return
    end

    if !music.persisted?
      music = MusicConverter.new(music).convert
      music.save
    end

    redirect_to music
  end
end
