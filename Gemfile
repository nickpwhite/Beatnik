source 'https://rubygems.org'
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby '2.7.6'

gem 'bootsnap', '>= 1.4.4', require: false
gem 'excon', '~> 0.85'
gem 'hashie', '~> 4.1'
gem 'importmap-rails'
gem 'jbuilder', '~> 2.7'
gem 'jwt', '~> 2.2'
gem 'pg', '~> 1.1'
gem 'puma', '~> 5.0'
gem 'rails', '~> 7.0.4'
gem 'rspotify', '~> 2.10'
gem 'sass-rails', '>= 6'
gem 'sidekiq', '~> 6.4'
gem 'slack-ruby-client', '~> 0.17'
gem 'sorbet-rails'
gem 'sorbet-runtime'
gem 'sprockets-rails'
gem 'stimulus-rails'
gem 'turbo-rails'

group :development, :test do
  gem 'pry-byebug', platforms: [:mri, :mingw, :x64_mingw]
end

group :development do
  gem 'listen', '~> 3.3'
  gem 'pry-rails'
  gem 'rack-mini-profiler', '~> 2.0'
  gem 'readline-ext'
  gem 'sorbet'
  gem 'spring'
  gem 'web-console', '>= 4.1.0'
end

group :test do
  gem 'capybara', '>= 3.26'
  gem 'selenium-webdriver'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]
