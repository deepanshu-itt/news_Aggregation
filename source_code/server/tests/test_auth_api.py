import unittest
from main import create_app 

class TestAuthAPI(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_login_user(self):
        response = self.client.post("/api/auth/login",json={
        "email": "deepanshu.p@intimetec.com",
        "password": "Deep0411@#"
        })
        self.assertEqual(response.get_json()["success"],True)
        self.client.post("/api/auth/logout")

    def test_duplicate_user_register(self):
        response = self.client.post("/api/auth/register",json={
        "email": "deepanshu.p@intimetec.com",
        "password": "Deep0411@#",
        'username': "Deep0481$%"
        })
        self.assertEqual(response.get_json()["success"],False)
    
    
    def test_new_user_register(self):
        response = self.client.post("/api/auth/register",json={
        "email": "deepanshu.p@hp.com",
        "password": "Deep0411@#",
        'username': "Deep0481$%"
        })

        self.assertEqual(response.get_json()["success"],False)
