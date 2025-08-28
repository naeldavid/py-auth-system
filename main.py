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
    print("\n" + "="*50)
    print("🚀 Python Authentication System Starting...")
    print("📍 Server URL: http://localhost:5001")
    print("📍 Network URL: http://0.0.0.0:5001")
    print("🔒 Secure Login Required")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)