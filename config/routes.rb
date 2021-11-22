# frozen_string_literal: true
# typed: strict

Rails.application.routes.draw do
  resources :music, only: [:show, :create]
  resources :settings, only: [:index, :create]

  get "/slack/authorize", to: 'slack#authorize'
  get "/about", to: 'home#about'
  get "/(:page)", to: 'home#index', as: :home
end
