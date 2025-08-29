#!/usr/bin/env python3
"""
Python Authentication System - Main Launcher
Enterprise-grade authentication with email 2FA
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from py.web_auth import app

if __name__ == '__main__':
    import socket
    
    # Get local IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "192.168.x.x"
    
    print("\n" + "="*50)
    print("🚀 Python Authentication System Starting...")
    print("📍 Local URL: http://localhost:8080")
    print(f"🌐 Network URL: http://{local_ip}:8080")
    print("🔒 Secure Login Required")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=8080)