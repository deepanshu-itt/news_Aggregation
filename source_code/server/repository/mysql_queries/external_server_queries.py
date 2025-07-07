create_external_server_query = """
            INSERT IGNORE INTO external_servers (name, api_key, base_url, status)
            VALUES (%s, %s, %s, %s)
        """


get_external_server_by_id_query = "SELECT * FROM external_servers WHERE id = %s"

get_external_server_by_name_query  = "SELECT * FROM external_servers WHERE name = %s"

get_all_external_servers = "SELECT * FROM external_servers"

update_external_server_query = """
                UPDATE external_servers
                SET status = %s, api_key = %s
                WHERE id = %s
            """

update_external_server_status_query = """
                UPDATE external_servers
                SET status = %s
                WHERE id = %s
            """

update_external_server_last_accessed_query = """
            UPDATE external_servers
            SET last_accessed = CURRENT_TIMESTAMP
            WHERE id = %s
        """