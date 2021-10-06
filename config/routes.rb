# typed: false
Rails.application.routes.draw do
  resources :music, only: [:show, :create]

  get "/about", to: 'home#about'
  get "/(:page)", to: 'home#index'
end
