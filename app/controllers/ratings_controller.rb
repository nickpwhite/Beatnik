# frozen_string_literal: true
# typed: strict

class RatingsController < ApplicationController
  class CreateParams < T::Struct
    const :music_id, Integer
    const :rating, Integer
  end

  sig {void}
  def create
    typed_params = TypedParams[CreateParams].new.extract!(params)
    music = Music.find(typed_params.music_id)

    if rated?(music.id)
      redirect_to music
    else
      if typed_params.rating.positive?
        music.match_rating += 1
      elsif typed_params.rating.negative?
        music.match_rating -= 1
      end

      music.save!
      set_rated(music.id)

      redirect_to music
    end
  end
end
