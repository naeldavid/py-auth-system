import re
import requests

class PasswordValidator:
    def __init__(self):
        self.common_passwords = set()
        self._load_common_passwords()
    
    def _load_common_passwords(self):
        # Load from local file or use basic list
        common = ['password', '123456', 'admin', 'root', 'qwerty', 'letmein']
        self.common_passwords.update(common)
    
    def validate(self, password):
        errors = []
        
        if len(password) < 12:
            errors.append("Password must be at least 12 characters")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain uppercase letters")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain lowercase letters")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain numbers")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain special characters")
        
        if password.lower() in self.common_passwords:
            errors.append("Password is too common")
        
        return len(errors) == 0, errors