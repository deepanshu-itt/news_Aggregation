

create_news_article_query = """
        INSERT INTO news_articles (title, description, url, image_url, published_at, source, category_id, raw_data, is_hidden, report_count, views)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, 0, 0)
        """

get_article_by_url_query = "SELECT * FROM news_articles WHERE url = %s"

get_article_by_id_query = """
SELECT 
    a.id,
    a.title,
    a.description,
    a.url,
    a.image_url,
    a.published_at,
    a.source,
    a.category_id,
    a.raw_data,
    a.created_at,
    a.views,
    a.is_hidden,
    a.report_count,
    c.name AS category_name,
    COALESCE(SUM(CASE WHEN ar.reaction = 'like' THEN 1 ELSE 0 END), 0) AS like_count,
    COALESCE(SUM(CASE WHEN ar.reaction = 'dislike' THEN 1 ELSE 0 END), 0) AS dislike_count
FROM 
    news_articles a
LEFT JOIN 
    article_reactions ar ON a.id = ar.article_id
LEFT JOIN
    categories c ON a.category_id = c.id
WHERE 
    a.id = %s
GROUP BY 
    a.id
"""

update_article_view_query = """ UPDATE news_articles
                    SET views = views + 1
                    WHERE id = %s;
                """

get_all_articles_query = """
        SELECT na.*, c.name AS category_name
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        WHERE 1=1
        """
        

get_article_by_date_range_query = """
            SELECT 
                na.*, 
                c.name AS category_name,
                COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
                COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
            FROM news_articles na
            JOIN categories c ON na.category_id = c.id
            LEFT JOIN article_reactions ar ON na.id = ar.article_id
            WHERE na.is_hidden != 1 AND na.published_at BETWEEN %s AND %s
            GROUP BY na.id 
            ORDER BY na.published_at DESC
        """

get_article_by_keyword_query = """
        SELECT 
            na.*, 
            c.name AS category_name,
            COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
            COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        LEFT JOIN article_reactions ar ON na.id = ar.article_id
        WHERE na.is_hidden != 1 AND (na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s)
        GROUP BY na.id
        ORDER BY na.published_at DESC
        """

get_article_by_keyword_and_range_query = """
        SELECT 
            na.*, 
            c.name AS category_name,
            COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
            COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
        FROM news_articles na
        JOIN categories c ON na.category_id = c.id
        LEFT JOIN article_reactions ar ON na.id = ar.article_id
        WHERE na.is_hidden != 1 AND  na.published_at BETWEEN %s AND %s AND (na.title LIKE %s OR na.description LIKE %s OR na.raw_data LIKE %s)
        GROUP BY na.id
        ORDER BY na.published_at DESC
        """

get_user_saved_Article_query = """
        SELECT 
            na.*, 
            c.name AS category_name,
            COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
            COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count
        FROM saved_articles sa
        JOIN news_articles na ON sa.article_id = na.id
        JOIN categories c ON na.category_id = c.id
        LEFT JOIN article_reactions ar ON na.id = ar.article_id
        WHERE na.is_hidden != 1 AND sa.user_id = %s 
        GROUP BY na.id
        ORDER BY sa.saved_at DESC
        """

hide_article_by_keyword_table_query = """UPDATE news_articles
                    SET is_hidden = 1
                    WHERE EXISTS (
                        SELECT 1
                        FROM article_filters
                        WHERE news_articles.title LIKE CONCAT('%', article_filters.keyword, '%')
                    )"""

hide_article_by_category_query = """ UPDATE news_articles na
                    JOIN categories c ON na.category_id = c.id
                    SET na.is_hidden = 1
                    WHERE c.is_hidden = 1
                """


get_article_by_date_and_category_query = """
            SELECT 
                na.*, 
                c.name AS category_name,
                COALESCE(SUM(ar.reaction = 'like'), 0) AS like_count,
                COALESCE(SUM(ar.reaction = 'dislike'), 0) AS dislike_count,
                (
                    CASE WHEN JSON_CONTAINS(un.category_preferences, JSON_QUOTE(c.name)) THEN 3 ELSE 0 END
                    +
                    CASE 
                        WHEN JSON_CONTAINS(un.category_preferences, JSON_QUOTE(c.name)) 
                            AND (na.title LIKE CONCAT('%', c.name, '%') 
                            OR na.description LIKE CONCAT('%', c.name, '%')) THEN 2
                        ELSE 0 
                    END
                    +
                    CASE WHEN sa.article_id IS NOT NULL THEN 2 ELSE 0 END
                    +
                    CASE WHEN ar_filter.article_id IS NOT NULL THEN 1 ELSE 0 END
                ) AS relevance_score

            FROM news_articles na
            JOIN categories c ON na.category_id = c.id
            LEFT JOIN article_reactions ar ON na.id = ar.article_id
            LEFT JOIN user_notifications un ON un.user_id = %s
            LEFT JOIN saved_articles sa ON sa.article_id = na.id AND sa.user_id = %s
            LEFT JOIN article_reactions ar_filter ON ar_filter.article_id = na.id AND ar_filter.user_id = %s AND ar_filter.reaction = 'like'

            WHERE na.is_hidden != 1 AND na.published_at BETWEEN %s AND %s
        """


hide_article_by_keyword_query = """
                        UPDATE news_articles AS na
                        JOIN (
                            SELECT id FROM news_articles
                            WHERE (title LIKE %s OR description LIKE %s OR raw_data LIKE %s)
                        ) AS subquery ON na.id = subquery.id
                        SET na.is_hidden = 1"""