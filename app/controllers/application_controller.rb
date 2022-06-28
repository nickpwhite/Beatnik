# frozen_string_literal: true
# typed: strict

class ApplicationController < ActionController::Base
  before_action :initialize_visitor

  sig {void}
  private def initialize_visitor
    return if session[:visitor_id].present?

    session[:visitor_id] = SecureRandom.uuid
  end

  sig {params(music_id: Integer).returns(T::Boolean)}
  def rated?(music_id)
    !!session["rated.#{music_id}".to_sym]
  end

  sig {params(music_id: Integer).void}
  def set_rated(music_id)
    session["rated.#{music_id}".to_sym] = true
  end
end
