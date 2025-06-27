from typing import Optional

class CursorDto:
    
    def __init__(self, query: str, params = None, fetch_one: Optional [bool] = False,
                 fetch_all: Optional[bool] = False, commit : Optional[bool] = False):
        
        self.query = query
        self.params = params
        self.fetch_one = fetch_one
        self.fetch_all = fetch_all
        self.commit = commit
