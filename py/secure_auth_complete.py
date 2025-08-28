import hashlib
import json
import os
import secrets
import time
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple, Set
from enum import Enum
import getpass

# Security Configuration
class SecurityConfig:
    PASSWORD_MIN_LENGTH = 8
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_DURATION = 300  # 5 minutes
    SESSION_TIMEOUT = 1800  # 30 minutes
    SALT_LENGTH = 32
    TOKEN_LENGTH = 32

# RBAC System
class Permission(Enum):
    READ_FILES = "read_files"
    WRITE_FILES = "write_files"
    DELETE_FILES = "delete_files"
    ADMIN_PANEL = "admin_panel"
    USER_MANAGEMENT = "user_management"

class Role(Enum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class RBACSystem:
    def __init__(self):
        self.role_permissions = {
            Role.GUEST: {Permission.READ_FILES},
            Role.USER: {Permission.READ_FILES, Permission.WRITE_FILES},
            Role.ADMIN: {Permission.READ_FILES, Permission.WRITE_FILES, 
                        Permission.DELETE_FILES, Permission.ADMIN_PANEL},
            Role.SUPER_ADMIN: set(Permission)
        }
    
    def has_permission(self, user_role: str, permission: Permission) -> bool:
        try:
            role = Role(user_role)
            return permission in self.role_permissions[role]
        except ValueError:
            return False

# Audit Logger
class SecurityAuditLogger:
    def __init__(self, log_file: str = "logs/security_audit.log"):
        self.log_file = log_file
        logging.basicConfig(filename=log_file, level=logging.INFO,
                          format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('SecurityAudit')
    
    def log_event(self, event_type: str, username: str, details: Dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "username": username,
            "details": details
        }
        self.logger.info(json.dumps(event))

# Main Database and Authentication System
class SecureUserDatabase:
    def __init__(self, db_file: str = "data/secure_users.json"):
        self.db_file = db_file
        self.users = self._load_users()
        self.failed_attempts = {}
        self.active_sessions = {}
        self.rbac = RBACSystem()
        self.audit_logger = SecurityAuditLogger()
    
    def _load_users(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return self._create_default_users()
    
    def _create_default_users(self) -> Dict:
        salt = secrets.token_hex(SecurityConfig.SALT_LENGTH)
        default_users = {
            "nael": {
                "password_hash": self._hash_password_with_salt("password", salt),
                "salt": salt,
                "security_pin_hash": self._hash_password_with_salt("000", salt),
                "email": "nael@example.com",
                "role": "admin",
                "mfa_enabled": True,
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "files": ["document1.txt", "project.py", "notes.md"]
            }
        }
        self._save_users(default_users)
        return default_users
    
    def _save_users(self, users: Dict):
        with open(self.db_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _hash_password_with_salt(self, password: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def _generate_session_token(self) -> str:
        return secrets.token_urlsafe(SecurityConfig.TOKEN_LENGTH)
    
    def _is_account_locked(self, username: str) -> bool:
        if username not in self.failed_attempts:
            return False
        
        attempts, last_attempt = self.failed_attempts[username]
        if attempts >= SecurityConfig.MAX_LOGIN_ATTEMPTS:
            if time.time() - last_attempt < SecurityConfig.LOCKOUT_DURATION:
                return True
            else:
                del self.failed_attempts[username]
        return False
    
    def _record_failed_attempt(self, username: str):
        current_time = time.time()
        if username in self.failed_attempts:
            attempts, _ = self.failed_attempts[username]
            self.failed_attempts[username] = (attempts + 1, current_time)
        else:
            self.failed_attempts[username] = (1, current_time)
        
        if self.failed_attempts[username][0] >= SecurityConfig.MAX_LOGIN_ATTEMPTS:
            self.audit_logger.log_event("ACCOUNT_LOCKOUT", username, {})
    
    def authenticate_user(self, username: str, password: str, security_pin: str) -> Tuple[bool, Optional[str], str]:
        if self._is_account_locked(username):
            return False, None, "Account temporarily locked due to failed attempts"
        
        if username not in self.users:
            self._record_failed_attempt(username)
            self.audit_logger.log_event("LOGIN_ATTEMPT", username, {"success": False})
            return False, None, "Invalid credentials"
        
        user_data = self.users[username]
        salt = user_data["salt"]
        
        password_hash = self._hash_password_with_salt(password, salt)
        pin_hash = self._hash_password_with_salt(security_pin, salt)
        
        if (password_hash == user_data["password_hash"] and 
            pin_hash == user_data["security_pin_hash"]):
            
            if username in self.failed_attempts:
                del self.failed_attempts[username]
            
            session_token = self._generate_session_token()
            self.active_sessions[session_token] = {
                "username": username,
                "created_at": time.time(),
                "last_activity": time.time()
            }
            
            self.users[username]["last_login"] = datetime.now().isoformat()
            self._save_users(self.users)
            
            self.audit_logger.log_event("LOGIN_ATTEMPT", username, {"success": True})
            self.audit_logger.log_event("SESSION_CREATED", username, {"session_token": session_token[:16] + "..."})
            
            return True, session_token, "Authentication successful"
        else:
            self._record_failed_attempt(username)
            self.audit_logger.log_event("LOGIN_ATTEMPT", username, {"success": False})
            return False, None, "Invalid credentials"
    
    def validate_session(self, token: str) -> Tuple[bool, Optional[str]]:
        if token not in self.active_sessions:
            return False, None
        
        session = self.active_sessions[token]
        current_time = time.time()
        
        # Handle both datetime and float timestamps
        last_activity = session["last_activity"]
        if isinstance(last_activity, datetime):
            last_activity = last_activity.timestamp()
        
        if current_time - last_activity > SecurityConfig.SESSION_TIMEOUT:
            username = session["username"]
            del self.active_sessions[token]
            self.audit_logger.log_event("SESSION_EXPIRED", username, {"session_token": token[:16] + "..."})
            return False, None
        
        session["last_activity"] = current_time
        return True, session["username"]
    
    def logout(self, token: str):
        if token in self.active_sessions:
            username = self.active_sessions[token]["username"]
            del self.active_sessions[token]
            self.audit_logger.log_event("LOGOUT", username, {"session_token": token[:16] + "..."})
    
    def get_user_data(self, username: str) -> Optional[Dict]:
        return self.users.get(username)

# CLI Authentication System
class SecureAuthenticationSystem:
    def __init__(self):
        self.db = SecureUserDatabase()
        self.current_session = None
    
    def login(self) -> Optional[str]:
        print("=== Secure Authentication System ===")
        
        try:
            username = input("Username: ").strip()
            if not username:
                print("Username cannot be empty.")
                return None
            
            password = getpass.getpass("Password: ")
            security_pin = getpass.getpass("Security PIN: ")
            
            success, token, message = self.db.authenticate_user(username, password, security_pin)
            
            if success:
                self.current_session = token
                print(f"✓ {message}")
                return username
            else:
                print(f"✗ {message}")
                return None
                
        except KeyboardInterrupt:
            print("\nLogin cancelled.")
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def display_security_info(self, username: str):
        user_data = self.db.get_user_data(username)
        if user_data:
            print(f"\n=== Welcome, {username} ===")
            print(f"Role: {user_data['role']}")
            print(f"Email: {user_data['email']}")
            print(f"MFA Enabled: {'Yes' if user_data['mfa_enabled'] else 'No'}")
            print(f"Last Login: {user_data.get('last_login', 'Never')}")
            print(f"Files: {', '.join(user_data['files'])}")

def main():
    auth_system = SecureAuthenticationSystem()
    logged_in_user = auth_system.login()
    
    if logged_in_user:
        auth_system.display_security_info(logged_in_user)
    else:
        print("Access denied.")

if __name__ == "__main__":
    main()