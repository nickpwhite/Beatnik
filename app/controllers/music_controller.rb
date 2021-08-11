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

    render :show, locals: {music: music}
  end
end
