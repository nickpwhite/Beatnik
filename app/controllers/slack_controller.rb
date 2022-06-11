# frozen_string_literal: true
# typed: strict

class SlackController < ApplicationController
  skip_before_action :verify_authenticity_token, only: :event

  class AuthorizeParams < T::Struct
    const :code, String
  end

  class EventParams < T::Struct
    const :token, String
    const :team_id, String
    const :api_app_id, String
    const :event, T::Hash[String, T.untyped]
    const :type, String
    const :event_id, String
    const :event_time, Integer
  end

  sig {void}
  def authorize
    typed_params = TypedParams[AuthorizeParams].new.extract!(params)
    code = typed_params.code

    slack_bot = Slack::Utils.perform_oauth(code)
    if slack_bot.nil?
      flash.alert = "Something went wrong connecting to Slack."
    elsif slack_bot.persisted?
      flash.notice =
        "The Beatnik Bot already exists in your Slack workspace "\
        "#{slack_bot.team_name}."
    elsif slack_bot.save
      flash.notice =
        "The Beatnik Bot was successfully created in your Slack workspace "\
        "#{slack_bot.team_name}."
    else
      flash.alert = "Something went wrong connecting to Slack."
    end

    redirect_to home_url
  end

  sig {void}
  def event
    Slack::Events::Request.new(request).verify!

    if params.include?(:challenge)
      render plain: params[:challenge]
      return
    end

    typed_params = TypedParams[EventParams].new.extract!(params)
    event_params = typed_params.event
    event_type = T.cast(event_params["type"], String)
    event =
      case event_type
      when "app_uninstalled"
        AppUninstalledEvent.from_params(event_params)
      when "link_shared"
        LinkSharedEvent.from_params(event_params)
      else
        raise "Unsupported event type #{type}"
      end
    event_container = SlackEventContainer.create!(
      token: typed_params.token,
      team_id: typed_params.team_id,
      api_app_id: typed_params.api_app_id,
      type: typed_params.type,
      event_id: typed_params.event_id,
      event_time: typed_params.event_time,
      slack_event: event,
    )
    SlackEventJob.perform_async(event_container.id)

    head :ok
  rescue Slack::Events::Request::TimestampExpired, Slack::Events::Request::InvalidSignature
    head :forbidden
  end
end
