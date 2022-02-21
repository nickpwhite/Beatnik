# frozen_string_literal: true
# typed: strict

module SoundcloudAPI
  class Client
    include Singleton

    sig do
      params(
        url: String,
        pattern: String
      )
      .returns(
        Nokogiri::HTML5::Document
      )
    end
    private def _get(url, pattern='//h2')
      browser = Watir::Browser.new :firefox, options: {args: ['-headless']}
      browser.goto(url)
      document = parse_html(browser, pattern: pattern, num_retries: 2)
      browser.close
      document
    end

    sig {params(url: String).returns(T::Hash[String, T.untyped])}
    def get_album(url)
      document = _get(url)

      {
        'name' => get_name(document),
        'artist' => get_artist(document),
        'artwork' => get_artwork(document),
      }
    end

    sig {params(url: String).returns(T::Hash[String, T.untyped])}
    def get_track(url)
      document = _get(url)

      {
        'name' => get_name(document),
        'artist' => get_artist(document),
        'artwork' => get_artwork(document),
        'album' => get_album_name(document),
      }
    end

    sig do
      params(
        title: String,
        artist_name: String
      )
      .returns(
        T.nilable(String)
      )
    end
    def search_album(title, artist_name)
      query = "#{title} #{artist_name}".gsub(' & ', '+').gsub(/\s/, '+')
      document = _get(
        "https://soundcloud.com/search/albums?q=#{query}",
        'div.searchList > ul'
      )

      path = document.css('a.soundTitle__title')&.first&.[]('href')

      if path.present?
        "https://soundcloud.com#{path}"
      end
    end

    sig do
      params(
        title: String,
        artist_name: String
      )
      .returns(
        T.nilable(String)
      )
    end
    def search_track(title, artist_name)
      query = "#{title} #{artist_name}".gsub(' & ', '+').gsub(/\s/, '+')

      document = _get(
        "https://soundcloud.com/search/sounds?q=#{query}",
        'div.searchList > ul',
      )

      path = document.css('a.soundTitle__title')&.first&.[]('href')

      if path.present?
        "https://soundcloud.com#{path}"
      end
    end

    sig do
      params(
        browser: Watir::Browser,
        pattern: String,
        num_retries: Integer
      )
      .returns(Nokogiri::HTML5::Document)
    end
    private def parse_html(browser, pattern:, num_retries: 0)
      document = Nokogiri::HTML5(browser.html)
      if document.search(pattern).blank? && num_retries > 0
        sleep 1
        document = parse_html(
          browser, pattern: pattern, num_retries: num_retries - 1
        )
      end
      document
    end

    sig {params(document: Nokogiri::HTML5::Document).returns(String)}
    private def get_name(document)
      document
        .xpath('//h1[contains(@class,"soundTitle__title")]/span/text()')
        .to_s
        .strip
    end

    sig {params(document: Nokogiri::HTML5::Document).returns(String)}
    private def get_artist(document)
      document
        .xpath('//h2[contains(@class,"soundTitle__username")]/a/text()')
        .to_s
        .strip
        .presence
    end

    sig {params(document: Nokogiri::HTML5::Document).returns(String)}
    private def get_artwork(document)
      document
        .xpath('//span[contains(@class, "sc-artwork")]')
        .attribute('style')
        .value
        .match(/background-image: url\("(.*)"\);/)[1]
    end

    sig {params(document: Nokogiri::HTML5::Document).returns(T.nilable(String))}
    private def get_album_name(document)
      document
        .xpath('//span[contains(@class, "inPlaylist__title")]/text()')
        .to_s
        .strip
        .presence
    end
  end
end
