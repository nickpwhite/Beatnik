# frozen_string_literal: true
# typed: strict

class HomeController < ApplicationController
  class IndexParams < T::Struct
    const :page, T.nilable(Integer)
  end

  sig {void}
  def index
    typed_params = TypedParams[IndexParams].new.extract!(params)

    current_page = typed_params.page || 0
    last_page = (Music.for_feed.count / Music::PAGE_SIZE).ceil - 1
    page_range = case current_page
                 when 0
                   [current_page, current_page + 1, current_page + 2]
                 when last_page
                   [current_page - 2, current_page - 1, current_page]
                 else
                   [current_page - 1, current_page, current_page + 1]
                 end
    latest_music = Music.get_feed(current_page)

    render :index, locals: {
      latest_music: latest_music,
      current_page: current_page,
      last_page: last_page,
      page_range: page_range,
    }
  end
end
