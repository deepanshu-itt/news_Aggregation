import unittest
from main import create_app 
class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    def test_login_user(self):
        response = self.client.post("/api/auth/login",json={
        "email": "deepanshu.p@intimetec.com",
        "password": "Deep0411@#"
        })
        self.assertEqual(response.get_json()["success"],True)

    
    def test_user_preferences(self):
        self.test_login_user()
        response = self.client.get("/api/user/userpreferences")
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_valid_update_user_preferences(self):
        self.test_login_user()
        response = self.client.put("/api/user/notifications",json = {
            'keywords' : "Business"
        })
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_valid_article_save(self):
        self.test_login_user()
        response = self.client.post("/api/user/articles/save",json = {
            'article_id' : 92
        })
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_valid_article_unsave(self):
        self.test_login_user()
        response = self.client.post("/api/user/articles/save",json = {
            'article_id' : 92
        })
        self.assertEqual(response.get_json()["success"],True)

    
    def test_get_news_articles(self):
        self.test_login_user()
        response = self.client.get("/api/user/news")
        self.assertEqual(response.get_json()["success"],True)
        response = self.client.get("/api/user/news?q=AI")
        self.assertEqual(response.get_json()["success"],True)
        response = self.client.get("/api/user/news?category=technology")
        self.assertEqual(response.get_json()["success"],True)
        response = self.client.get("/api/user/news?start_date=2025-06-17&end_date=2025-06-18")
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_get_Categories(self):
        self.test_login_user()
        response = self.client.get("/api/user/categories")
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_get_notifications(self):
        self.test_login_user()
        response = self.client.get("/api/user/notifications")
        self.assertEqual(response.get_json()["success"],True)
        
    def test_get_saved_articles(self):
        self.test_login_user()
        response = self.client.get("/api/user/articles/saved")
        self.assertEqual(response.get_json()[0]["success"],True)
