class BaseAdminAction:
    def __init__(self, api_client, get_current_user):
        self.api_client = api_client
        self.get_current_user = get_current_user

    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")
