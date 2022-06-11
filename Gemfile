source 'https://rubygems.org'
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby '2.7.6'

gem 'bootsnap', '>= 1.4.4', require: false
gem 'excon', '~> 0.85'
gem 'hashie', '~> 4.1'
gem 'jbuilder', '~> 2.7'
gem 'jwt', '~> 2.2'
gem 'pg', '~> 1.1'
gem 'puma', '~> 5.0'
gem 'rails', '~> 6.1.4'
gem 'rspotify', '~> 2.10'
gem 'sass-rails', '>= 6'
gem 'slack-ruby-client', '~> 0.17'
gem 'sorbet-rails'
gem 'sorbet-runtime'
gem 'turbolinks', '~> 5'
gem 'watir', '~> 6.19'
gem 'webdrivers', '~> 4.5'
gem 'webpacker', '~> 5.0'

group :development, :test do
  gem 'pry-byebug', platforms: [:mri, :mingw, :x64_mingw]
end

group :development do
  gem 'listen', '~> 3.3'
  gem 'rack-mini-profiler', '~> 2.0'
  gem 'pry-rails'
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

gem "sidekiq", "~> 6.4"
