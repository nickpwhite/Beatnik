# typed: ignore
class AddSourceToMusic < ActiveRecord::Migration[6.1]
  def change
    reversible do |dir|
      dir.up do
        execute <<~SQL
          CREATE TYPE music_source AS ENUM (
            'apple_music', 'soundcloud', 'spotify', 'tidal', 'youtube_music'
          );
        SQL
      end
      dir.down { execute "DROP TYPE music_source;" }
    end

    add_column :beatnik_music, :source, :music_source
  end
end
