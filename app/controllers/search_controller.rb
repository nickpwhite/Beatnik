# frozen_string_literal: true
# typed: strict

class SearchController < ApplicationController
  class Params < T::Struct
    const :q, String
  end

  sig {void}
  def index
    typed_params = TypedParams[Params].new.extract!(params)

    uri = URI.parse(typed_params.q)
    if uri.is_a?(URI::Beatnik)
      convert_url(uri)
    else
      results = SearchClient.instance.search(typed_params.q)
      render locals: {query: typed_params.q, results: results}
    end
  end

  def convert_url(uri)
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
