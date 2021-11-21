# typed: strict
class ApplicationController < ActionController::Base
  before_action :initialize_visitor

  sig {void}
  private def initialize_visitor
    return if session[:visitor_id].present?

    session[:visitor_id] = SecureRandom.uuid
  end
end
