# frozen_string_literal: true
# typed: strict

class SlackEventJob
  include Sidekiq::Job

  sig {params(event_container_id: Integer).void}
  def perform(event_container_id)
    event_container = SlackEventContainer.includes(:slack_event).find(event_container_id)
    slack_bot = SlackBot.find_by(team_id: event_container.team_id)
    if slack_bot.nil?
      logger.info("Slack bot not found for team_id #{event_container.team_id}, returning")
      return
    end

    event_container.slack_event.process(slack_bot)
  end
end
