# frozen_string_literal: true
# typed: strict

class SearchClient
  include Singleton

  sig {params(query: String).returns(T::Array[SearchResult])}
  def search(query)
    Client::Spotify.search(query).map {|hash| SearchResult.new(**hash)}
  end

  class SearchResult < T::Struct
    const :name, String
    const :url, String
    const :artist, String
    const :artwork, String
    const :album, T.nilable(String)
  end
end
