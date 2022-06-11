# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2022_06_05_173450) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "api_request", id: :serial, force: :cascade do |t|
    t.text "user_agent"
    t.string "ip_address", limit: 45
    t.string "referer", limit: 200
    t.text "query_string", null: false
    t.text "query", null: false
    t.text "path"
  end

  create_table "app_uninstalled_events", force: :cascade do |t|
    t.string "type", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "auth_group", id: :serial, force: :cascade do |t|
    t.string "name", limit: 150, null: false
    t.index ["name"], name: "auth_group_name_a6ea08ec_like", opclass: :varchar_pattern_ops
    t.index ["name"], name: "auth_group_name_key", unique: true
  end

  create_table "auth_group_permissions", id: :serial, force: :cascade do |t|
    t.integer "group_id", null: false
    t.integer "permission_id", null: false
    t.index ["group_id", "permission_id"], name: "auth_group_permissions_group_id_permission_id_0cd325b0_uniq", unique: true
    t.index ["group_id"], name: "auth_group_permissions_group_id_b120cbf9"
    t.index ["permission_id"], name: "auth_group_permissions_permission_id_84c5c92e"
  end

  create_table "auth_permission", id: :serial, force: :cascade do |t|
    t.string "name", limit: 255, null: false
    t.integer "content_type_id", null: false
    t.string "codename", limit: 100, null: false
    t.index ["content_type_id", "codename"], name: "auth_permission_content_type_id_codename_01ab375a_uniq", unique: true
    t.index ["content_type_id"], name: "auth_permission_content_type_id_2f476e4b"
  end

  create_table "auth_user", id: :serial, force: :cascade do |t|
    t.string "password", limit: 128, null: false
    t.datetime "last_login"
    t.boolean "is_superuser", null: false
    t.string "username", limit: 150, null: false
    t.string "first_name", limit: 30, null: false
    t.string "last_name", limit: 150, null: false
    t.string "email", limit: 254, null: false
    t.boolean "is_staff", null: false
    t.boolean "is_active", null: false
    t.datetime "date_joined", null: false
    t.index ["username"], name: "auth_user_username_6821ab7c_like", opclass: :varchar_pattern_ops
    t.index ["username"], name: "auth_user_username_key", unique: true
  end

  create_table "auth_user_groups", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "group_id", null: false
    t.index ["group_id"], name: "auth_user_groups_group_id_97559544"
    t.index ["user_id", "group_id"], name: "auth_user_groups_user_id_group_id_94350c0c_uniq", unique: true
    t.index ["user_id"], name: "auth_user_groups_user_id_6a12ed8b"
  end

  create_table "auth_user_user_permissions", id: :serial, force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "permission_id", null: false
    t.index ["permission_id"], name: "auth_user_user_permissions_permission_id_1fbb5f2c"
    t.index ["user_id", "permission_id"], name: "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq", unique: true
    t.index ["user_id"], name: "auth_user_user_permissions_user_id_a95ead1b"
  end

  create_table "beatnik_music", id: :serial, force: :cascade do |t|
    t.string "music_type", limit: 1, null: false
    t.string "name", limit: 200, null: false
    t.string "artist", limit: 200, null: false
    t.string "album", limit: 200, null: false
    t.string "apple_url", limit: 200
    t.string "gpm_url", limit: 200
    t.string "soundcloud_url", limit: 200
    t.string "spotify_url", limit: 200
    t.integer "match_rating", null: false
    t.string "artwork", limit: 200, null: false
    t.string "tidal_url", limit: 200
    t.string "ytm_url", limit: 200
    t.enum "source"
    t.index ["apple_url"], name: "beatnik_music_apple_url_4b8de405_like", opclass: :varchar_pattern_ops
    t.index ["apple_url"], name: "beatnik_music_apple_url_4b8de405_uniq", unique: true
    t.index ["gpm_url"], name: "beatnik_music_gpm_url_e7c1ac2c_like", opclass: :varchar_pattern_ops
    t.index ["gpm_url"], name: "beatnik_music_gpm_url_e7c1ac2c_uniq", unique: true
    t.index ["soundcloud_url"], name: "beatnik_music_soundcloud_url_64d68bec_like", opclass: :varchar_pattern_ops
    t.index ["soundcloud_url"], name: "beatnik_music_soundcloud_url_64d68bec_uniq", unique: true
    t.index ["spotify_url"], name: "beatnik_music_spotify_url_c2a182ee_like", opclass: :varchar_pattern_ops
    t.index ["spotify_url"], name: "beatnik_music_spotify_url_c2a182ee_uniq", unique: true
    t.index ["tidal_url"], name: "beatnik_music_tidal_url_cd13b47b_like", opclass: :varchar_pattern_ops
    t.index ["tidal_url"], name: "beatnik_music_tidal_url_key", unique: true
    t.index ["ytm_url"], name: "beatnik_music_ytm_url_28445fad_like", opclass: :varchar_pattern_ops
    t.index ["ytm_url"], name: "beatnik_music_ytm_url_key", unique: true
  end

  create_table "django_admin_log", id: :serial, force: :cascade do |t|
    t.datetime "action_time", null: false
    t.text "object_id"
    t.string "object_repr", limit: 200, null: false
    t.integer "action_flag", limit: 2, null: false
    t.text "change_message", null: false
    t.integer "content_type_id"
    t.integer "user_id", null: false
    t.index ["content_type_id"], name: "django_admin_log_content_type_id_c4bce8eb"
    t.index ["user_id"], name: "django_admin_log_user_id_c564eba6"
    t.check_constraint "action_flag >= 0", name: "django_admin_log_action_flag_check"
  end

  create_table "django_content_type", id: :serial, force: :cascade do |t|
    t.string "app_label", limit: 100, null: false
    t.string "model", limit: 100, null: false
    t.index ["app_label", "model"], name: "django_content_type_app_label_model_76bd3d3b_uniq", unique: true
  end

  create_table "django_migrations", id: :serial, force: :cascade do |t|
    t.string "app", limit: 255, null: false
    t.string "name", limit: 255, null: false
    t.datetime "applied", null: false
  end

  create_table "django_session", primary_key: "session_key", id: { type: :string, limit: 40 }, force: :cascade do |t|
    t.text "session_data", null: false
    t.datetime "expire_date", null: false
    t.index ["expire_date"], name: "django_session_expire_date_a5c62663"
    t.index ["session_key"], name: "django_session_session_key_c0390e0f_like", opclass: :varchar_pattern_ops
  end

  create_table "link_shared_events", force: :cascade do |t|
    t.string "type", null: false
    t.string "channel", null: false
    t.string "user", null: false
    t.text "links", default: [], null: false, array: true
    t.string "thread_ts", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "settings", force: :cascade do |t|
    t.string "visitor_id", null: false
    t.enum "redirect", default: "none", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["visitor_id"], name: "index_settings_on_visitor_id"
  end

  create_table "slack_event_containers", force: :cascade do |t|
    t.string "token", null: false
    t.string "team_id", null: false
    t.string "api_app_id", null: false
    t.string "type", null: false
    t.string "event_id", null: false
    t.integer "event_time", null: false
    t.string "slack_event_type"
    t.bigint "slack_event_id"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["slack_event_type", "slack_event_id"], name: "index_slack_event_containers_on_slack_event"
  end

  create_table "slackbot_install", id: :serial, force: :cascade do |t|
    t.text "app_id", null: false
    t.text "authed_user_id", null: false
    t.text "scope", null: false
    t.text "access_token", null: false
    t.text "bot_user_id", null: false
    t.text "team_name", null: false
    t.text "team_id", null: false
    t.index ["team_id"], name: "slackbot_in_team_id_9e5616_idx"
    t.index ["team_id"], name: "slackbot_install_team_id_0352d183_like", opclass: :text_pattern_ops
    t.index ["team_id"], name: "slackbot_install_team_id_0352d183_uniq", unique: true
  end

  create_table "tracking_pageview", id: :serial, force: :cascade do |t|
    t.text "url", null: false
    t.text "referer"
    t.text "query_string"
    t.string "method", limit: 20
    t.datetime "view_time", null: false
    t.string "visitor_id", limit: 40, null: false
    t.index ["visitor_id"], name: "tracking_pageview_visitor_id_a78682e5"
    t.index ["visitor_id"], name: "tracking_pageview_visitor_id_a78682e5_like", opclass: :varchar_pattern_ops
  end

  create_table "tracking_visitor", primary_key: "session_key", id: { type: :string, limit: 40 }, force: :cascade do |t|
    t.string "ip_address", limit: 39, null: false
    t.text "user_agent"
    t.datetime "start_time", null: false
    t.integer "expiry_age"
    t.datetime "expiry_time"
    t.integer "time_on_site"
    t.datetime "end_time"
    t.integer "user_id"
    t.index ["session_key"], name: "tracking_visitor_session_key_8cd35282_like", opclass: :varchar_pattern_ops
    t.index ["user_id"], name: "tracking_visitor_user_id_68f9235e"
  end

  add_foreign_key "auth_group_permissions", "auth_group", column: "group_id", name: "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id"
  add_foreign_key "auth_group_permissions", "auth_permission", column: "permission_id", name: "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm"
  add_foreign_key "auth_permission", "django_content_type", column: "content_type_id", name: "auth_permission_content_type_id_2f476e4b_fk_django_co"
  add_foreign_key "auth_user_groups", "auth_group", column: "group_id", name: "auth_user_groups_group_id_97559544_fk_auth_group_id"
  add_foreign_key "auth_user_groups", "auth_user", column: "user_id", name: "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id"
  add_foreign_key "auth_user_user_permissions", "auth_permission", column: "permission_id", name: "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm"
  add_foreign_key "auth_user_user_permissions", "auth_user", column: "user_id", name: "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id"
  add_foreign_key "django_admin_log", "auth_user", column: "user_id", name: "django_admin_log_user_id_c564eba6_fk_auth_user_id"
  add_foreign_key "django_admin_log", "django_content_type", column: "content_type_id", name: "django_admin_log_content_type_id_c4bce8eb_fk_django_co"
  add_foreign_key "tracking_pageview", "tracking_visitor", column: "visitor_id", primary_key: "session_key", name: "tracking_pageview_visitor_id_a78682e5_fk_tracking_"
  add_foreign_key "tracking_visitor", "auth_user", column: "user_id", name: "tracking_visitor_user_id_68f9235e_fk_auth_user_id"
end
