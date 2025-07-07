def merge_keywords_into_preferences(existing_preferences, category_name, new_keywords):
    category_to_update = find_category(existing_preferences, category_name)

    if category_to_update:
        updated_category = get_updated_category(category_to_update, new_keywords)
        updated_preferences = rebuild_preferences_with_updated_category(
            existing_preferences, updated_category
        )
    else:
        updated_preferences = add_new_category_if_missing(
            existing_preferences, category_name, new_keywords
        )

    return updated_preferences


def find_category(preferences, category_name):
    for category in preferences:
        if category['name'].lower() == category_name.lower():
            return category
    return None


def get_updated_category(category, new_keywords):
    merged_keywords = merge_keywords_lists(category.get('keywords', []), new_keywords)
    return {
        "name": category['name'],
        "enabled": category.get('enabled', True),
        "keywords": merged_keywords
    }


def rebuild_preferences_with_updated_category(preferences, updated_category):
    return [
        updated_category if c['name'].lower() == updated_category['name'].lower() else c
        for c in preferences
    ]


def add_new_category_if_missing(preferences, category_name, new_keywords):
    new_category = {
        "name": category_name,
        "enabled": True,
        "keywords": list(set(new_keywords))
    }
    return preferences + [new_category]


def merge_keywords_lists(existing_keywords, new_keywords):
    return list(set(existing_keywords) | set(new_keywords))


def remove_keywords_from_category(preferences_list, category_name, user_input_keywords):
    updated_preferences = []
    keyword_removed = False

    for category in preferences_list:
        if category['name'].lower() == category_name.lower():
            updated_category, removed = filter_out_keywords(category, user_input_keywords)
            keyword_removed = removed
            updated_preferences.append(updated_category)
        else:
            updated_preferences.append(category)

    return updated_preferences, keyword_removed


def filter_out_keywords(category, keywords_to_remove):
    original_keywords = category.get('keywords', [])
    filtered_keywords = [
        kw for kw in original_keywords
        if kw.lower() not in map(str.lower, keywords_to_remove)
    ]
    removed = len(filtered_keywords) != len(original_keywords)

    updated_category = {
        "name": category['name'],
        "enabled": category.get('enabled', True),
        "keywords": filtered_keywords
    }

    return updated_category, removed


def remove_category_from_preferences(preferences_list, category_name):
    return [
        category for category in preferences_list
        if category['name'].lower() != category_name.lower()
    ]
