# Secure Authentication System

Enterprise-grade authentication system with CLI and web interfaces.

## Features

- **Advanced Security**: PBKDF2 hashing, session management, account lockout
- **RBAC**: Role-based access control with permissions
- **Audit Logging**: Complete security event tracking
- **Multi-Interface**: Both CLI and web interfaces
- **Session Management**: Secure token-based sessions
- **MFA Support**: Multi-factor authentication ready

## Quick Start

### CLI Version
```bash
python secure_auth_complete.py
```

### Web Version
```bash
pip install Flask==2.3.3
python web_auth.py
```
Then visit: http://localhost:5000

## Default Credentials
- Username: `nael`
- Password: `password`  
- Security PIN: `000`

## File Structure
```
├── secure_auth_complete.py  # Complete CLI system
├── web_auth.py             # Flask web application
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   └── dashboard.html
├── static/                 # CSS/JS assets
└── secure_users.json      # User database (auto-generated)
```

## Security Features
- PBKDF2 password hashing (100,000 iterations)
- Account lockout after 3 failed attempts
- Session timeout (30 minutes)
- Comprehensive audit logging
- Role-based permissions
- Secure session tokens

## API Endpoints
- `GET /` - Login page
- `POST /login` - Authentication
- `GET /dashboard` - User dashboard
- `GET /logout` - Logout
- `GET /api/user/<username>` - User info API