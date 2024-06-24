module Jekyll
  module CategoryFilter
    def filter_by_category(posts, category)
      posts.select { |post| post['categories'] && post['categories'].include?(category) }
    end
  end
end

Liquid::Template.register_filter(Jekyll::CategoryFilter)
