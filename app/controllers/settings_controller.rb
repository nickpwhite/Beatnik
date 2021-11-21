# frozen_string_literal: true
# typed: strict

class SettingsController < ApplicationController
  class CreateParams < T::Struct
    class SettingsParam < T::Struct
      const :redirect, Settings::Redirect
    end

    const :settings, SettingsParam
  end

  sig {void}
  def index
    settings = Settings.find_or_initialize_by(visitor_id: session[:visitor_id])

    render :index, locals: {settings: settings}
  end

  sig {void}
  def create
    typed_params = TypedParams[CreateParams].new.extract!(params)
    settings = Settings.find_or_initialize_by(visitor_id: session[:visitor_id])

    settings.typed_redirect = typed_params.settings.redirect
    settings.save

    render "index", locals: {settings: settings}
  end
end
