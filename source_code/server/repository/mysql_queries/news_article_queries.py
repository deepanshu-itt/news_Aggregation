

create_news_article_query = """
        INSERT INTO news_articles (title, description, url, image_url, published_at, source, category_id, raw_data, is_hidden, report_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, 0)
        """