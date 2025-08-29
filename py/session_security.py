import secrets
import time
import jwt
from datetime import datetime, timedelta

class SecureSessionManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.active_sessions = {}
        self.session_history = {}
    
    def create_jwt_token(self, username, ip, fingerprint):
        """Create JWT token with claims"""
        payload = {
            'username': username,
            'ip': ip,
            'fingerprint': fingerprint,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1),
            'jti': secrets.token_urlsafe(16)  # JWT ID for revocation
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token, ip, fingerprint):
        """Verify JWT token with additional checks"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Verify IP and fingerprint
            if payload.get('ip') != ip:
                return False, 'IP mismatch'
            if payload.get('fingerprint') != fingerprint:
                return False, 'Device mismatch'
            
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, 'Token expired'
        except jwt.InvalidTokenError:
            return False, 'Invalid token'
    
    def create_secure_session(self, username, ip, fingerprint):
        """Create secure session with multiple tokens"""
        access_token = self.create_jwt_token(username, ip, fingerprint)
        refresh_token = secrets.token_urlsafe(32)
        session_id = secrets.token_urlsafe(16)
        
        session_data = {
            'username': username,
            'ip': ip,
            'fingerprint': fingerprint,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'created_at': time.time(),
            'last_activity': time.time(),
            'login_count': self.session_history.get(username, {}).get('count', 0) + 1
        }
        
        self.active_sessions[session_id] = session_data
        
        # Update session history
        if username not in self.session_history:
            self.session_history[username] = {'count': 0, 'last_login': None}
        self.session_history[username]['count'] += 1
        self.session_history[username]['last_login'] = time.time()
        
        return session_id, access_token, refresh_token
    
    def validate_session(self, session_id, ip, fingerprint):
        """Validate session with security checks"""
        if session_id not in self.active_sessions:
            return False, 'Session not found'
        
        session = self.active_sessions[session_id]
        
        # Check IP and fingerprint
        if session['ip'] != ip or session['fingerprint'] != fingerprint:
            del self.active_sessions[session_id]
            return False, 'Security violation'
        
        # Check session timeout
        if time.time() - session['last_activity'] > 1800:  # 30 minutes
            del self.active_sessions[session_id]
            return False, 'Session expired'
        
        # Update last activity
        session['last_activity'] = time.time()
        return True, session['username']
    
    def revoke_session(self, session_id):
        """Revoke specific session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def revoke_all_sessions(self, username):
        """Revoke all sessions for user"""
        sessions_to_remove = [
            sid for sid, session in self.active_sessions.items()
            if session['username'] == username
        ]
        for sid in sessions_to_remove:
            del self.active_sessions[sid]