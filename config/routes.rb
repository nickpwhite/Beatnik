# typed: false
Rails.application.routes.draw do
  get "/(:page)", to: 'home#index'

  resources :music, only: [:show]
end
