class CreateAppUninstalledEvents < ActiveRecord::Migration[6.1]
  def change
    create_table :app_uninstalled_events do |t|
      t.string :type, null: false

      t.timestamps
    end
  end
end
