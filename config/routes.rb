# frozen_string_literal: true
# typed: strict

Rails.application.routes.draw do
  resources :music, only: [:show]
  resources :search, only: [:index]
  resources :settings, only: [:index, :create]

  get "/slack/authorize", to: 'slack#authorize'
  post "/slack/event", to: 'slack#event'
  get "/about", to: 'home#about'
  get "/(:page)", to: 'home#index', as: :home
end
