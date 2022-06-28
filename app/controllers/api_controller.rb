# frozen_string_literal: true
# typed: strict

class ApiController < ApplicationController
  class ConvertParams < T::Struct
    const :q, String
  end

  def convert
    typed_params = TypedParams[ConvertParams].new.extract!(params)

    uri = URI.parse(typed_params.q)
    if uri.is_a?(URI::Beatnik)
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

      response_body = {
        errors: [],
        id: music.id,
        type: music.humanized_type,
        'album_art': music.artwork,
        'title': music.name,
        'artist': music.artist,
        'apple': music.apple_url,
        'soundcloud': music.soundcloud_url,
        'spotify': music.spotify_url,
        'tidal': music.tidal_url,
        'youtube_music': music.ytm_url
      }

      render json: response_body
    else
      render status: :bad_request
    end
  end
end
