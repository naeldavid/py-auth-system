import time
from collections import defaultdict
from functools import wraps
from flask import request, jsonify

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.blocked_ips = {}
    
    def is_rate_limited(self, ip, max_requests=5, window=60):
        now = time.time()
        # Clean old requests
        self.requests[ip] = [req_time for req_time in self.requests[ip] if now - req_time < window]
        
        if len(self.requests[ip]) >= max_requests:
            self.blocked_ips[ip] = now + 300  # Block for 5 minutes
            return True
        
        self.requests[ip].append(now)
        return False

rate_limiter = RateLimiter()

def rate_limit(max_requests=5, window=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.environ.get('REMOTE_ADDR')
            if rate_limiter.is_rate_limited(ip, max_requests, window):
                return jsonify({'error': 'Rate limit exceeded'}), 429
            return f(*args, **kwargs)
        return decorated_function
    return decorator