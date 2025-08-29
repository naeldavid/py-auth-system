# py-auth-system

Military-grade Python authentication system with advanced security features, biometric authentication, threat detection, and enterprise-level protection.

## 🚀 Features

### 🔐 Military-Grade Security
- **PBKDF2 Password Hashing** (100,000 iterations)
- **Multi-Factor Authentication** (Email 2FA + TOTP + Biometric)
- **WebAuthn Support** (Fingerprint, Face ID, Security Keys)
- **JWT Tokens** with device validation
- **Device Fingerprinting** and anomaly detection
- **IP Geolocation** and reputation checking
- **Real-Time Threat Detection** and blocking
- **CSRF Protection** and security headers
- **Rate Limiting** and brute force protection
- **Encrypted Data** at rest and in transit

### 👥 Advanced User Management
- **Role-Based Access Control** (RBAC)
- **Admin Panel** with real-time monitoring
- **Multi-Device Session Management**
- **Biometric Registration** and management
- **Security Event Dashboard**
- **User Activity Analytics**
- **Automated Backup System**

### 🌐 Modern Interface
- **Responsive Web Interface** with modern UI
- **CLI Interface** for terminal access
- **Real-Time Dashboard** with charts and metrics
- **Admin Panel** with system monitoring
- **Mobile-Friendly** design
- **Dark/Light Theme** support

### 📧 Communication & Alerts
- **Professional 2FA Emails** with HTML templates
- **TOTP App Integration** (Google Authenticator, Authy)
- **Real-Time Security Alerts**
- **Login Notifications** for new devices
- **Threat Detection Alerts**
- **System Health Notifications**

## 🚀 Quick Start

### Web Version (Recommended)
```bash
pip install Flask==2.3.3
python main.py
```
Then visit: http://localhost:5001

## 🔑 Default Admin Account
- Username: `admin`
- Password: `root`
- Security PIN: `9873`
- Role: `admin`

## 📁 Project Structure
```
py-auth-system/
├── main.py                    # Main launcher
├── py/                        # Core modules
│   ├── secure_auth_complete.py  # Core authentication
│   ├── web_auth.py           # Flask web app
│   ├── security_enhanced.py  # Advanced security
│   ├── session_security.py   # JWT & sessions
│   ├── biometric_auth.py     # WebAuthn support
│   ├── security_middleware.py # Security headers
│   ├── rate_limiter.py       # Rate limiting
│   ├── password_validator.py # Password policies
│   ├── monitoring.py         # System monitoring
│   └── backup_manager.py     # Automated backups
├── templates/                # Modern HTML templates
├── static/                  # Enhanced UI assets
│   ├── css/modern.css       # Modern styling
│   └── js/security-enhancements.js
├── config/                  # Configuration files
│   ├── requirements.txt     # Dependencies
│   └── security_config.yaml # Security policies
├── data/                    # Database files
├── logs/                    # Security & audit logs
├── tests/                   # Test suite
├── docker/                  # Container support
└── user_files/              # User file storage
```

## 🔒 Security Features

### 🔐 Authentication Layers
- **Password + PIN + Email 2FA + TOTP + Biometric**
- **WebAuthn Support** (Fingerprint, Face ID, Security Keys)
- **Device Fingerprinting** with anomaly detection
- **JWT Tokens** with device validation
- **Multi-Session Management** with automatic cleanup

### 🚫 Threat Protection
- **Real-Time IP Reputation** checking
- **Brute Force Protection** with automatic blocking
- **Rate Limiting** per IP and globally
- **Honeypot Endpoints** for attack detection
- **CSRF Protection** with secure tokens
- **XSS & Injection Prevention**

### 📊 Monitoring & Analytics
- **Real-Time Threat Detection**
- **Behavioral Analytics** for anomaly detection
- **Security Event Dashboard**
- **System Health Monitoring**
- **Automated Backup System**
- **Compliance Reporting** (SOC2, GDPR)

## 🌐 API Endpoints

### Authentication
- `GET /` - Modern login page
- `POST /login` - Multi-factor authentication
- `GET /login_2fa` - 2FA verification with countdown
- `POST /verify_2fa` - TOTP/Email code verification
- `POST /auth/webauthn/register` - Biometric registration
- `POST /auth/webauthn/verify` - Biometric authentication
- `GET /logout` - Secure session termination

### Security & Monitoring
- `GET /health` - System health check
- `POST /security/report` - Report suspicious activity
- `GET /admin/security` - Security dashboard
- `GET /admin/threats` - Threat detection logs
- `POST /admin/block-ip` - Manual IP blocking

### User Management
- `GET /dashboard` - Real-time user dashboard
- `POST /change_password` - Enhanced password change
- `GET /admin/users` - Advanced user management
- `POST /create_user` - User creation with MFA setup
- `POST /delete_user` - Secure user deletion
- `GET /admin/sessions` - Active session management

### System Management
- `GET /admin/metrics` - System performance metrics
- `POST /admin/backup` - Manual backup creation
- `GET /admin/audit` - Security audit logs
- `POST /admin/config` - Security configuration updates

## ⚙️ Configuration

### Security Configuration
Edit `config/security_config.yaml` to customize:
- **Password Policies** - Length, complexity, expiry
- **MFA Settings** - TOTP, biometric, backup codes
- **Rate Limits** - Login attempts, request limits
- **Threat Detection** - IP blocking, anomaly thresholds
- **Session Management** - Timeouts, concurrent sessions
- **Compliance** - SOC2, GDPR, audit settings

### Email & TOTP Setup
1. Configure SMTP in `py/email_sender.py`
2. Generate TOTP secrets for users
3. Set up WebAuthn domain configuration
4. Configure threat intelligence APIs

## 🛡️ Security Best Practices

- ✅ **Multi-Layer Security** - Use all available authentication methods
- ✅ **Regular Security Audits** - Review logs and threat reports
- ✅ **Device Management** - Register and monitor trusted devices
- ✅ **Network Security** - Monitor IP reputation and geolocation
- ✅ **Backup Strategy** - Automated encrypted backups
- ✅ **Incident Response** - Real-time threat detection and blocking
- ✅ **Compliance** - Follow SOC2, GDPR, and industry standards
- ✅ **Zero Trust** - Verify every request and session

## 📊 Enterprise Admin Features

- **Real-Time Security Dashboard** with threat visualization
- **Advanced User Management** with device tracking
- **System Performance Monitoring** with alerts
- **Threat Intelligence Integration** with IP reputation
- **Automated Backup Management** with encryption
- **Compliance Reporting** for SOC2, GDPR
- **Multi-Session Management** across devices
- **Biometric Device Registration** and management

## 🎮 Stream Deck Integration

Launch directly from Stream Deck with:
```bash
python3 /Users/--/Documents/py-auth-system/main.py
```

## 📦 Installation

### Quick Start
```bash
git clone <repository>
cd py-auth-system
pip install -r config/requirements.txt
python main.py
```

### Docker Deployment
```bash
docker build -f docker/Dockerfile -t py-auth-system .
docker run -p 5001:5001 py-auth-system
```

### Production Setup
1. **Configure Security**: Edit `config/security_config.yaml`
2. **Set Environment Variables**: Database, email, API keys
3. **Enable HTTPS**: Configure SSL certificates
4. **Set up Monitoring**: Configure threat intelligence APIs
5. **Test Security**: Run `python -m pytest tests/`

### System Requirements
- Python 3.8+
- 2GB RAM minimum
- SSL certificate for production
- SMTP server for email notifications

---
