import unittest
from main import create_app 
from dto.email_dto import EmailNotificationDto
from dto.news_article_dto import NewsArticleDto


class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    def test_login_user(self):
        response = self.client.post("/api/auth/login",json={
        "email": "deepanshu.p@intimetec.com",
        "password": "Deep0411@#"
        })
        headers = {
        "Authorization": "Bearer your_admin_token"  
        }
        response = response.get_json()
        user = response['user']
        headers['X-User-Id'] = user['id']
        headers['X-User-Role'] = user['role']
        self.assertEqual(response["success"],True)
        return headers

    
    def test_user_preferences(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/userpreferences", headers = headers )
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_insert_user_preferences(self):
        headers = self.test_login_user()
        response = self.client.put("/api/user/notifications", headers =headers,json ={
            'category_name': 'Travel',
            'keywords': "Germany"
        })
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_delete_user_preferences(self):
        headers = self.test_login_user()
        response = self.client.delete("/api/user/notifications", headers =headers,json = {
            'category_name': 'Travel',
            'keywords': "Germany"
        })
        self.assertEqual(response.get_json()["success"],True)


    def test_valid_article_save(self):
        headers = self.test_login_user()
        response = self.client.post("/api/user/articles/save",json = {
            'article_id' : 2666
        },headers = headers)
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_valid_article_unsave(self):
        headers = self.test_login_user()
        response = self.client.post("/api/user/articles/unsave",json = {
            'article_id' : 2666
        },headers = headers)
        self.assertEqual(response.get_json()["success"],True)

    
    def test_get_news_articles_by_query(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/news?q=AI",headers = headers)
        response = response.get_json()
        self.assertEqual(response["success"], True)
    
    
    def test_get_news_articles_by_date_range(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/news?start_date=2025-06-17&end_date=2025-06-18",headers = headers)
        response = response.get_json()
        self.assertEqual(response["success"], True)
    
    
    def test_get_news_articles_by_category(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/news?start_date=2025-06-17&end_date=2025-06-18&category=Technology",headers = headers)
        response = response.get_json()
        self.assertEqual(response["success"], True)

    
    def test_get_Categories(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/categories",headers = headers)
        response = response.get_json()
        self.assertEqual(response["success"],True)
    
    
    def test_get_notifications(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/notifications",headers = headers)
        self.assertEqual(response.get_json()["success"],True)
        
    def test_get_saved_articles(self):
        headers = self.test_login_user()
        response = self.client.get("/api/user/articles/saved",headers = headers,
                        json = {'keyword': "Amazon"})
        self.assertEqual(response.get_json()[0]["success"],True)
    
    
    def test_report_article(self):
        headers = self.test_login_user()
        response = self.client.post("/api/user/articles/2617/report",headers = headers,
                                   json = {'reason': 'vulgar'})
        response = response.get_json()
        if response == 'Article 2617 already reported.':
            self.assertEqual(response, "Article 2617 already reported.")
        else:
            self.assertEqual(response, "Article 2617 Reported successfully.")
    
    
    def test_unreport_article(self):
        headers = self.test_login_user()
        response = self.client.post("/api/user/articles/2617/unreport",headers = headers)
        response = response.get_json()
        self.assertEqual(response, "Article 2617 unreported successfully.")
    
    
    def test_like_article(self):
        headers = self.test_login_user()
        response = self.client.post("/api/user/articles/2679/react",headers = headers,
                                   json = {'reaction': 'like'})
        self.assertEqual(response.get_json()["success"],True)
    
    
    def test_unlike_article(self):
        headers = self.test_login_user()
        response = self.client.post("/api/user/articles/2679/react",headers = headers,
                                   json = {'reaction': 'dislike'})
        
        self.assertEqual(response.get_json()["success"],True)

    
    def test_dtos(self):
        EmailNotificationDto(user_id=2, article_ids=2666, message="Test Data")
        NewsArticleDto(title = "Hi", description ="test", url = "http", image_url="http", published_at= "2025-01-1", source = "2025-01-1", 
                 category_id=2)
        