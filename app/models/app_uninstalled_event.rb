# frozen_string_literal: true
# typed: strict

class AppUninstalledEvent < ApplicationRecord
  include SlackEvent

  self.inheritance_column = :_none

  has_one :slack_event_container, as: :slack_event

  sig {override.params(event: T::Hash[String, T.untyped]).returns(T.attached_class)}
  def self.from_params(event)
    create!(type: T.cast(event["type"], String))
  end

  sig {override.params(slack_bot: SlackBot).void}
  def process(slack_bot)
    slack_bot.destroy!
  end
end
