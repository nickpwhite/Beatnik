# frozen_string_literal: true
# typed: strict

class SearchClient
  include Singleton

  sig {params(query: String).returns(T::Array[Music])}
  def search(query)
    []
  end
end
