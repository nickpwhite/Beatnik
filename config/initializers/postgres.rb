# frozen_string_literal: true
# typed: strict

require "active_record/connection_adapters/postgresql_adapter"

ActiveRecord::ConnectionAdapters::PostgreSQLAdapter::
  NATIVE_DATABASE_TYPES[:enum] = { name: "enum" }
