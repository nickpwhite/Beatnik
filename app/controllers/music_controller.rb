# frozen_string_literal: true
# typed: strict

class MusicController < ApplicationController
  class ShowParams < T::Struct
    const :id, Integer
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
end
