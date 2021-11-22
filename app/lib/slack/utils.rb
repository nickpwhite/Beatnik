# frozen_string_literal: true
# typed: strict

module Slack
  module Utils
    extend T::Sig

    sig {returns(URI)}
    def self.oauth_url
      URI::HTTPS.build(
        host: "slack.com",
        path: "/oauth/v2/authorize",
        query: Rack::Utils.build_nested_query(query_params)
      )
    end

    sig {returns({client_id: String, scope: String, redirect_uri: String})}
    def self.query_params
      {
        client_id: client_id,
        scope: "chat:write,links:read",
        redirect_uri: redirect_uri,
      }
    end

    sig {params(code: String).returns(T.nilable(SlackBot))}
    def self.perform_oauth(code)
      response = Slack::Web::Client.new.oauth_v2_access(
        code: code,
        client_id: client_id,
        client_secret: client_secret,
        redirect_uri: redirect_uri,
      )

      if response.ok?
        SlackBot.find_or_initialize_by(team_id: response.team.id) do |slack_bot|
          slack_bot.app_id = response.app_id
          slack_bot.authed_user_id = response.authed_user.id
          slack_bot.scope = response.scope
          slack_bot.access_token = response.access_token
          slack_bot.bot_user_id = response.bot_user_id
          slack_bot.team_name = response.team.name
        end
      end
    end

    sig {returns(String)}
    private_class_method def self.client_id
      ENV.fetch('SLACK_CLIENT_ID')
    end

    sig {returns(String)}
    private_class_method def self.client_secret
      ENV.fetch('SLACK_CLIENT_SECRET')
    end

    sig {returns(String)}
    private_class_method def self.redirect_uri
      "https://cef4-157-131-154-125.ngrok.io/slack/authorize"
    end
  end
end
