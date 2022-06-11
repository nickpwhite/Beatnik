class CreateSlackEventContainers < ActiveRecord::Migration[6.1]
  def change
    create_table :slack_event_containers do |t|
      t.string :token, null: false
      t.string :team_id, null: false
      t.string :api_app_id, null: false
      t.string :type, null: false
      t.string :event_id, null: false
      t.integer :event_time, null: false
      t.references :slack_event, polymorphic: true

      t.timestamps
    end
  end
end
