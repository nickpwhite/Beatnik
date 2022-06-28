# frozen_string_literal: true
# typed: strict

Rails.application.routes.draw do
  resources :music, only: [:show] do
    resources :ratings, only: [:create]
  end
  resources :search, only: [:index]
  resources :settings, only: [:index, :create]

  get "/about", to: 'home#about'
  get "/api/convert", to: 'api#convert'
  get "/slack/authorize", to: 'slack#authorize'
  post "/slack/event", to: 'slack#event'
  get "/(:page)", to: 'home#index', as: :home
end
