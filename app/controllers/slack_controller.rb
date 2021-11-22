# frozen_string_literal: true
# typed: strict

class SlackController < ApplicationController
  class AuthorizeParams < T::Struct
    const :code, String
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
end
