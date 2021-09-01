# frozen_string_literal: true
# typed: strict

module Client
  class InvalidURIError < StandardError
  end

  class Base
    extend T::Helpers

    abstract!

    sig {abstract.params(music: Music).returns(Music)}
    def self.get_metadata(music); end

    sig {abstract.params(music: Music).returns(Music)}
    def self.get_url(music); end

    sig {params(uri: URI::Generic).returns(String)}
    private_class_method def self.path(uri)
      uri.path || raise(InvalidURIError)
    end
  end
end
