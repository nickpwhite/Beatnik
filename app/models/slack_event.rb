# frozen_string_literal: true
# typed: strict

module SlackEvent
  extend T::Sig
  extend T::Helpers
  interface!

  module ClassMethods
    extend T::Sig
    extend T::Helpers
    abstract!

    sig {abstract.params(event: T::Hash[String, T.untyped]).returns(T.attached_class)}
    def from_params(event); end
  end
  mixes_in_class_methods ClassMethods

  sig {abstract.params(slack_bot: SlackBot).void}
  def process(slack_bot); end
end
