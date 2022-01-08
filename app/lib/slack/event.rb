# frozen_string_literal: true
# typed: strict

module Slack::Event
  extend T::Sig

  class UnsupportedEventError < StandardError; end

  RawHash = T.type_alias {T::Hash[String, T.untyped]}

  sig do
    params(event_params: SlackController::EventParams)
    .returns(EventContainer[T.any(AppUninstalled, LinkShared)])
  end
  def self.create_event(event_params)
    event = build_event(event_params.event)

    EventContainer.new(
      event: event,
      token: event_params.token,
      team_id: event_params.team_id,
      api_app_id: event_params.api_app_id,
      type: event_params.type,
      event_id: event_params.event_id,
      event_time: event_params.event_time
    )
  end

  sig {params(event: RawHash).returns(T.any(AppUninstalled, LinkShared))}
  def self.build_event(event)
    type = T.cast(event["type"], String)
    case type
    when "app_uninstalled"
      AppUninstalled.new(type: type)
    when "link_shared"
      links = T.cast(event["links"], T::Array[{"url" => String, "domain" => String}])
      LinkShared.new(
        type: type,
        channel: T.cast(event["channel"], String),
        user: T.cast(event["user"], String),
        links: links.map {|l| URI.parse(l["url"])},
        thread_ts: T.cast(event["thread_ts"] || event["message_ts"], String),
      )
    else
      raise UnsupportedEventError.new("Unsupported event type #{type}")
    end
  end

  class EventContainer < T::Struct
    extend T::Generic

    EventType = type_member

    const :event, EventType
    const :token, String
    const :team_id, String
    const :api_app_id, String
    const :type, String
    const :event_id, String
    const :event_time, Integer

    sig {void}
    def process
      slack_bot = SlackBot.find_by(team_id: team_id)
      return if slack_bot.nil?

      event.process(slack_bot)
    end
  end

  class AppUninstalled < T::Struct
    const :type, String

    sig {params(slack_bot: SlackBot).void}
    def process(slack_bot)
      slack_bot.destroy
    end
  end

  class LinkShared < T::Struct
    const :type, String
    const :channel, String
    const :user, String
    const :links, T::Array[URI::Generic]
    const :thread_ts, String

    sig {params(slack_bot: SlackBot).void}
    def process(slack_bot)
      return if channel == "COMPOSER" || slack_bot.bot_user_id == user

      uri = links.find {|l| l.is_a?(URI::Beatnik)}

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

      return if music.nil?

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

      lines.unshift("Here are some other links to this #{music.humanized_type}")

      Slack::Web::Client.new(token: slack_bot.access_token).chat_postMessage(
        channel: channel,
        thread_ts: thread_ts,
        text: lines.join("\n"),
        unfurl_links: false,
      )
    end
  end
end
