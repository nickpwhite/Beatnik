# frozen_string_literal: true
# typed: strict

module SoundcloudAPI
  class Scraper
    @name = T.let('soundcloud_scraper', String)
    @engine = T.let(:selenium_chrome, Symbol)
    @start_urls = T.let(["https://soundcloud.com"], T::Array[String])

    sig {params(response: T.untyped, url: T.untyped, data: T.untyped).void}
    def parse(response, url:, data: {})
      p response.class
      p url.class
      p data.class
    end
  end
end
