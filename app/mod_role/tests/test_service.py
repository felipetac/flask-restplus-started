import unittest
from app import create_app
from app.mod_role.service import Service

class RoleServiceTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')

    def test_list_role(self):
        with self.app.app_context():
            res = Service.list()
            assert "data" in res.keys()
