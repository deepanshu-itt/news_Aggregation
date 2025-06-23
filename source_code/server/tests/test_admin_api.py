import unittest
from main import create_app 

class TestAdminAPI(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_login_user(self):
        response = self.client.post("/api/auth/login",json={
        "email": "admin@example.com",
        "password": "Deep0411@#"
        })
        self.assertEqual(response.get_json()["success"],True)
        self.client.post("/api/auth/logout")
    
    
    def test_get_servers(self):
        self.test_login_user()
        response = self.client.get("/api/admin/external_servers")
        print(response.get_json())
        self.assertEqual(response.get_json()["success"],True)
    
    def test_get_servers(self):
        self.test_login_user()
        response = self.client.get("/api/admin/external_servers")
        print(response.get_json())
        self.assertEqual(response.get_json()["success"],True)
    
    def test_get_servers(self):
        self.test_login_user()
        response = self.client.get("/api/admin/external_servers")
        print(response.get_json())
        self.assertEqual(response.get_json()["success"],True)