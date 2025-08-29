from flask import request, jsonify, g
from functools import wraps
import time
import hashlib

class SecurityMiddleware:
    def __init__(self, app, security_manager, threat_detector):
        self.app = app
        self.security = security_manager
        self.threat_detector = threat_detector
        self.setup_middleware()
    
    def setup_middleware(self):
        @self.app.before_request
        def security_check():
            ip = request.environ.get('REMOTE_ADDR')
            path = request.path
            
            # Check if IP is blocked
            if ip in self.threat_detector.blocked_ips:
                return jsonify({'error': 'Access denied'}), 403
            
            # Check honeypot access
            if self.threat_detector.is_honeypot_access(path):
                self.threat_detector.block_ip(ip)
                return jsonify({'error': 'Not found'}), 404
            
            # Check brute force
            if self.threat_detector.is_brute_force(ip):
                self.threat_detector.block_ip(ip)
                return jsonify({'error': 'Too many requests'}), 429
            
            # Add security headers
            g.security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
                'Referrer-Policy': 'strict-origin-when-cross-origin'
            }
        
        @self.app.after_request
        def add_security_headers(response):
            if hasattr(g, 'security_headers'):
                for header, value in g.security_headers.items():
                    response.headers[header] = value
            return response

def require_mfa(f):
    """Decorator to require MFA for sensitive operations"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user has completed MFA recently
        if not hasattr(g, 'mfa_verified') or not g.mfa_verified:
            return jsonify({'error': 'MFA required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def log_security_event(event_type, details=None):
    """Log security events"""
    event = {
        'timestamp': time.time(),
        'type': event_type,
        'ip': request.environ.get('REMOTE_ADDR'),
        'user_agent': request.headers.get('User-Agent'),
        'details': details or {}
    }
    
    # In production, send to SIEM/logging system
    with open('logs/security_events.log', 'a') as f:
        f.write(f"{event}\n")

def check_csrf_token():
    """CSRF protection"""
    if request.method in ['POST', 'PUT', 'DELETE']:
        token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
        expected = request.cookies.get('csrf_token')
        
        if not token or not expected or token != expected:
            log_security_event('csrf_violation')
            return False
    return True