import unittest
from app import create_app

class RoleAPITests(unittest.TestCase):

    def setUp(self):
        self.client = create_app('testing').test_client()

    def test_list_role(self):
        response = self.client.get('/api/1/role/page/1')
        assert response.status_code == 401
