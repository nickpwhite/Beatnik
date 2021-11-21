# typed: strict
Rails.application.routes.draw do
  resources :music, only: [:show, :create]
  resources :settings, only: [:index, :create]

  get "/about", to: 'home#about'
  get "/(:page)", to: 'home#index'
end
