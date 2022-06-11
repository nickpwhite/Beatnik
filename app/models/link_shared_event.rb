# frozen_string_literal: true
# typed: strict

class LinkSharedEvent < ApplicationRecord
  include SlackEvent

  self.inheritance_column = :_none

  has_one :slack_event_container, as: :slack_event

  sig {override.params(event: T::Hash[String, T.untyped]).returns(T.attached_class)}
  def self.from_params(event)
    links = T.cast(event["links"], T::Array[{"url" => String, "domain" => String}])
    create!(
      type: T.cast(event["type"], String),
      channel: T.cast(event["channel"], String),
      user: T.cast(event["user"], String),
      links: links.map {URI.parse(_1["url"])},
      thread_ts: T.cast(event["thread_ts"] || event["message_ts"], String)
    )
  end

  sig {override.params(slack_bot: SlackBot).void}
  def process(slack_bot)
    return if channel == "COMPOSER" || slack_bot.bot_user_id == user

    links.each do |link|
      uri = URI.parse(link)
      next unless uri.is_a?(URI::Beatnik)

      music =
        case uri
        when URI::AppleMusic
          Music.find_or_initialize_by(apple_url: uri.to_s) do |music|
            music.typed_source = Music::Source::AppleMusic
          end
        when URI::Soundcloud
          Music.find_or_initialize_by(soundcloud_url: uri.to_s) do |music|
            music.typed_source = Music::Source::Soundcloud
          end
        when URI::Spotify
          Music.find_or_initialize_by(spotify_url: uri.to_s) do |music|
            music.typed_source = Music::Source::Spotify
          end
        when URI::Tidal
          Music.find_or_initialize_by(tidal_url: uri.to_s) do |music|
            music.typed_source = Music::Source::Tidal
          end
        when URI::YoutubeMusic
          Music.find_or_initialize_by(ytm_url: uri.to_s) do |music|
            music.typed_source = Music::Source::YoutubeMusic
          end
        end

      next if music.nil?

      if !music.persisted?
        music = MusicConverter.new(music).convert
        music.save
      end

      lines = [
        music.apple_url,
        music.soundcloud_url,
        music.spotify_url,
        music.tidal_url,
        music.ytm_url,
      ].compact.map {|url| ":headphones: #{url}"}

      lines.unshift("Here are some other links to #{music.name} by #{music.artist}")

      Slack::Web::Client.new(token: slack_bot.access_token).chat_postMessage(
        channel: channel,
        thread_ts: thread_ts,
        text: lines.join("\n"),
        unfurl_links: false,
      )
    end
  end
end
