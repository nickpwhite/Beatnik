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
    const :event, Slack::Event::RawHash
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
    Slack::Event.create_event(typed_params).process

    head :ok
  rescue Slack::Events::Request::TimestampExpired,
    Slack::Events::Request::InvalidSignature
    head :forbidden
  end
end
