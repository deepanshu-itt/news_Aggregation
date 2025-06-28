from services.category_service import CategoryService
from repository.category_repository import CategoryRepository

class CategoryIdentifier:
    
    @staticmethod
    def resolve_category_id(article, existing_categories, category_repository: CategoryRepository):
        category_service = CategoryService()

        category_id = (
            CategoryIdentifier._get_existing_or_new_category(article, existing_categories, category_repository)
            or CategoryIdentifier._get_category_from_text(article, category_service)
            or CategoryIdentifier._fallback_to_general(existing_categories, category_repository)
        )

        return category_id

    @staticmethod
    def _get_existing_or_new_category(article:dict, existing_categories, category_repository: CategoryRepository):
        category_name = article.get('category')
        if not category_name:
            return None

        category_name: str = category_name.lower()

        if category_name in existing_categories:
            return existing_categories[category_name]

        new_category = category_repository.create(category_name.capitalize())
        if new_category:
            existing_categories[new_category.name.lower()] = new_category.id
            print(f"Dynamically added new category: {new_category.name}")
            return new_category.id

        return None


    @staticmethod
    def _get_category_from_text(article, category_service: CategoryService):
        return category_service.identify_category_from_text(
            article.get('title', '') or '',
            article.get('description', '') or ''
        )


    @staticmethod
    def _fallback_to_general(existing_categories, category_repo):
        general_id = existing_categories.get('general')
        if general_id:
            return general_id

        general_cat = category_repo.create('General')
        if general_cat:
            existing_categories['general'] = general_cat.id
            print("Dynamically added 'General' category.")
            return general_cat.id

        print("Warning: Could not create 'General' category.")
        return None
