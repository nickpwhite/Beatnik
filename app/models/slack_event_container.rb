# frozen_string_literal: true
# typed: strict

class SlackEventContainer < ApplicationRecord
  self.inheritance_column = :_none

  belongs_to :slack_event, polymorphic: true
end
