upsert_reaction_query = """
        INSERT IGNORE INTO article_reactions (user_id, article_id, reaction)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE reaction = VALUES(reaction), reacted_at = CURRENT_TIMESTAMP
        """


get_reaction_count_query = """
        SELECT COUNT(*) as count FROM article_reactions
        WHERE article_id = %s AND reaction = %s
        """