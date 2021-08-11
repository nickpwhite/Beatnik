# typed: strict
class ApplicationRecord < ActiveRecord::Base
  extend T::Helpers

  abstract!

  self.abstract_class = true
end
