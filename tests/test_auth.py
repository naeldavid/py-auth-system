import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py.secure_auth_complete import SecureUserDatabase
from py.password_validator import PasswordValidator

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.db = SecureUserDatabase("test_users.json")
        self.validator = PasswordValidator()
    
    def test_password_validation(self):
        valid, errors = self.validator.validate("StrongP@ssw0rd123!")
        self.assertTrue(valid)
        
        valid, errors = self.validator.validate("weak")
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)
    
    def test_user_authentication(self):
        # Test with default admin user
        success, token, message = self.db.authenticate_user("admin", "root", "9873")
        self.assertTrue(success)
        self.assertIsNotNone(token)
    
    def test_session_validation(self):
        success, token, _ = self.db.authenticate_user("admin", "root", "9873")
        if success:
            valid, username = self.db.validate_session(token)
            self.assertTrue(valid)
            self.assertEqual(username, "admin")
    
    def tearDown(self):
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")

if __name__ == '__main__':
    unittest.main()