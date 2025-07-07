class Category:
    def __init__(self, id: int, name: str, is_hidden: bool):
        self.id = id
        self.name = name
        self.is_hidden = is_hidden
        

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_hidden": False
        }