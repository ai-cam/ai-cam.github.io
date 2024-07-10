module Jekyll
  module CustomFilters
    require 'time'

    def filter_by_category(posts, category)
      # Normalize to an array if single category string is provided
      categories = [category].flatten

      posts.select do |post|
        post_categories = post['categories'] || post['category']
        post_categories.is_a?(Array) && categories.all? { |cat| post_categories.include?(cat) }
      end
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
