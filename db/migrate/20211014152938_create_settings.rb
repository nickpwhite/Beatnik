# frozen_string_literal: true
# typed: true

class CreateSettings < ActiveRecord::Migration[6.1]
  def change
    reversible do |dir|
      dir.up do
        execute <<~SQL
          CREATE TYPE redirect AS ENUM (
            'none', 'apple_music', 'soundcloud', 'spotify', 'tidal', 'youtube_music'
          );
        SQL
      end
      dir.down { execute "DROP TYPE redirect;" }
    end

    create_table :settings do |t|
      t.string :visitor_id, null: false, index: true
      t.column :redirect, :redirect, null: false, default: "none"

      t.timestamps
    end
  end
end
