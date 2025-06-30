create_category_query = "INSERT INTO categories (name, is_hidden) VALUES (%s)"

find_by_name_query = "SELECT * FROM categories WHERE name = %s"

find_by_id_query = "SELECT * FROM categories WHERE id = %s"

get_all_categories_query = "SELECT * FROM categories ORDER BY id"

get_category_id_query = "SELECT id FROM categories WHERE name = %s"

hide_category_query = "update categories SET is_hidden = 1 WHERE id = %s"

unhide_category_query = "update categories SET is_hidden = 1 WHERE id = %s"