# typed: false
Rails.application.routes.draw do
  get "/(:page)", to: 'home#index'
end
