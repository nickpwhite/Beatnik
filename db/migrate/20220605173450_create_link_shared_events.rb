class CreateLinkSharedEvents < ActiveRecord::Migration[6.1]
  def change
    create_table :link_shared_events do |t|
      t.string :type, null: false
      t.string :channel, null: false
      t.string :user, null: false
      t.text :links, array: true, null: false, default: []
      t.string :thread_ts, null: false

      t.timestamps
    end
  end
end
