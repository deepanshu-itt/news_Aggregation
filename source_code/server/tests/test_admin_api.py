import unittest
from main import create_app 
from app_utils import load_external_server_keys_into_app_config


class TestAdminAPI(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()


    def test_login_user(self):
        response = self.client.post("/api/auth/login",json={
        "email": "admin@example.com",
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


    def test_get_servers(self):
        headers = self.test_login_user()
        response = self.client.get("/api/admin/external_servers", headers = headers)
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
    
    
    def test_create_category(self):
        headers = self.test_login_user()
        response = self.client.post("/api/admin/categories", headers = headers,
                                    json = {'name': "technology"})
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
    
    
    def test_update_server_status(self):
        headers = self.test_login_user()
        response = self.client.put("/api/admin/external_servers/1/status",headers = headers, 
                            json = {'status': "active", "api_key":"4f4cfc3e5a304539a3a78d8fe1811969"})
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
    
    
    def test_all_server_details(self):
        headers = self.test_login_user()
        response = self.client.get("/api/admin/external_servers/details",headers = headers)
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
    
    
    def test_hide_article(self):
        headers = self.test_login_user()
        response = self.client.get("/api/admin/hide_article/1901",headers = headers,
                        query_string={"token": "admin_token"})
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
    
    
    def test_hide_category(self):
        headers = self.test_login_user()
        response = self.client.post("/api/admin/hide_category_article",headers = headers,
                        json = {'name': "General"})
        response = response.get_json()
        self.assertEqual(response.get('success'),True)

    
    def test_unhide_category(self):
        headers = self.test_login_user()
        response = self.client.post("/api/admin/unhide_category_article",headers = headers,
                        json = {'name': "General"})
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
    
    
    def test_hide_article_by_keyword(self):
        headers = self.test_login_user()
        response = self.client.post("/api/admin/hide_article/keywords",headers = headers,
                        json = {'keyword': "Amazon"})
        response = response.get_json()
        self.assertEqual(response.get('success'),True)
