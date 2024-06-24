module Jekyll
  module CustomFilters
    require 'time'

    def filter_by_category(posts, category)
      posts.select { |post| post['categories'] && post['categories'].include?(category) }
    end

    def past_events(events)
      current_date = Time.now
      events.select do |event|
        event_end = Time.parse(event['end'])
        event_end < current_date
      end
    end

    def upcoming_events(events)
      current_date = Time.now
      events.select do |event|
        event_start = Time.parse(event['start'])
        event_start > current_date
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CustomFilters)
