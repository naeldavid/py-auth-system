import hashlib
import hmac
import base64
import time
import struct
import requests
import json
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class AdvancedSecurity:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.suspicious_ips = set()
        self.device_fingerprints = {}
    
    def generate_totp(self, secret, time_step=30):
        """Generate TOTP code"""
        timestamp = int(time.time() // time_step)
        message = struct.pack('>Q', timestamp)
        digest = hmac.new(base64.b32decode(secret), message, hashlib.sha1).digest()
        offset = digest[-1] & 0x0f
        code = struct.unpack('>I', digest[offset:offset+4])[0] & 0x7fffffff
        return str(code % 1000000).zfill(6)
    
    def verify_totp(self, secret, token, window=1):
        """Verify TOTP code with time window"""
        for i in range(-window, window + 1):
            timestamp = int(time.time() // 30) + i
            message = struct.pack('>Q', timestamp)
            digest = hmac.new(base64.b32decode(secret), message, hashlib.sha1).digest()
            offset = digest[-1] & 0x0f
            code = struct.unpack('>I', digest[offset:offset+4])[0] & 0x7fffffff
            if str(code % 1000000).zfill(6) == token:
                return True
        return False
    
    def get_device_fingerprint(self, request):
        """Generate device fingerprint"""
        user_agent = request.headers.get('User-Agent', '')
        accept_language = request.headers.get('Accept-Language', '')
        accept_encoding = request.headers.get('Accept-Encoding', '')
        
        fingerprint_data = f"{user_agent}|{accept_language}|{accept_encoding}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    def check_ip_reputation(self, ip):
        """Check IP against threat intelligence"""
        try:
            # Simulate threat intelligence check
            if ip in ['127.0.0.1', 'localhost']:
                return {'risk': 'low', 'country': 'Local'}
            
            # In production, use real threat intelligence APIs
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            data = response.json()
            
            risk = 'low'
            if data.get('proxy') or data.get('hosting'):
                risk = 'high'
            elif data.get('country') in ['CN', 'RU', 'KP']:  # High-risk countries
                risk = 'medium'
            
            return {
                'risk': risk,
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown')
            }
        except:
            return {'risk': 'unknown', 'country': 'Unknown'}
    
    def detect_anomaly(self, username, ip, fingerprint, login_time):
        """Detect login anomalies"""
        anomalies = []
        
        # Check for new device
        user_devices = self.device_fingerprints.get(username, set())
        if fingerprint not in user_devices:
            anomalies.append('new_device')
        
        # Check for suspicious IP
        if ip in self.suspicious_ips:
            anomalies.append('suspicious_ip')
        
        # Check for unusual time
        hour = datetime.fromtimestamp(login_time).hour
        if hour < 6 or hour > 22:  # Outside normal hours
            anomalies.append('unusual_time')
        
        return anomalies
    
    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive data"""
        return self.cipher.encrypt(json.dumps(data).encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Decrypt sensitive data"""
        return json.loads(self.cipher.decrypt(encrypted_data.encode()).decode())

class ThreatDetection:
    def __init__(self):
        self.failed_attempts = {}
        self.blocked_ips = set()
        self.honeypot_endpoints = {'/admin', '/wp-admin', '/.env', '/config'}
    
    def is_brute_force(self, ip, max_attempts=5, window=300):
        """Detect brute force attacks"""
        now = time.time()
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = []
        
        # Clean old attempts
        self.failed_attempts[ip] = [
            attempt for attempt in self.failed_attempts[ip] 
            if now - attempt < window
        ]
        
        return len(self.failed_attempts[ip]) >= max_attempts
    
    def record_failed_attempt(self, ip):
        """Record failed login attempt"""
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = []
        self.failed_attempts[ip].append(time.time())
    
    def is_honeypot_access(self, path):
        """Check if accessing honeypot endpoints"""
        return any(endpoint in path for endpoint in self.honeypot_endpoints)
    
    def block_ip(self, ip, duration=3600):
        """Block IP for specified duration"""
        self.blocked_ips.add(ip)
        # In production, integrate with firewall/WAF