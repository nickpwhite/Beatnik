# typed: false
Rails.application.routes.draw do
  resources :music, only: [:show, :create]

  get "/(:page)", to: 'home#index'
end
