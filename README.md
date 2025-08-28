# Python Authentication System

Enterprise-grade authentication system with advanced security features, email 2FA, and comprehensive user management.

## 🚀 Features

### 🔐 Advanced Security
- **PBKDF2 Password Hashing** (100,000 iterations)
- **Email 2FA** with cryptographically secure codes
- **Account Lockout** after 3 failed attempts (5-minute lockout)
- **Session Management** with 30-minute timeout
- **Encrypted Credentials** in source code
- **Audit Logging** for all security events

### 👥 User Management
- **Role-Based Access Control** (RBAC)
- **Admin Panel** for user creation/deletion
- **Custom Security PINs** for each user
- **File Management** per user
- **Password Change** functionality

### 🌐 Multi-Interface
- **Web Interface** with Bootstrap UI
- **CLI Interface** for terminal access
- **Text Editor** with file operations
- **Admin Dashboard** for user management

### 📧 Email Integration
- **Professional 2FA Emails** with HTML templates
- **Gmail SMTP** with encrypted credentials
- **5-minute code expiry** with automatic cleanup
- **One-time use codes** for maximum security

## 🚀 Quick Start

### Web Version (Recommended)
```bash
pip install Flask==2.3.3
python web_auth.py
```
Then visit: http://localhost:5001

### CLI Version
```bash
python secure_auth_complete.py
```

## 🔑 Default Admin Account
- Username: `nael`
- Password: `password`
- Security PIN: `000`
- Role: `admin`

## 📁 Project Structure
```
├── secure_auth_complete.py  # Core authentication system
├── web_auth.py             # Flask web application
├── email_sender.py         # Email 2FA functionality
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── login_2fa.html     # 2FA verification
│   ├── dashboard.html     # User dashboard
│   ├── admin_users.html   # Admin panel
│   └── editor.html        # Text editor
├── static/                # CSS/JS assets
│   ├── css/style.css      # Styling
│   └── js/               # JavaScript files
├── user_files/           # User file storage
├── secure_users.json     # User database
└── security_audit.log    # Security events
```

## 🔒 Security Features

### Authentication
- **Multi-factor Authentication** (Password + PIN + Email 2FA)
- **Cryptographically Secure** random code generation
- **Session Token** based authentication
- **Automatic Session Cleanup** on expiry

### Authorization
- **Role-Based Permissions** (Guest, User, Admin, Super Admin)
- **Protected Admin Routes** with role verification
- **File Access Control** per user

### Data Protection
- **Salted Password Hashing** with unique salts per user
- **Encrypted Email Credentials** in source code
- **No Credential Exposure** in APIs or logs
- **Secure File Storage** in user directories

## 🌐 API Endpoints

### Authentication
- `GET /` - Login page
- `POST /login` - User authentication
- `GET /login_2fa` - 2FA verification page
- `POST /verify_2fa` - 2FA code verification
- `POST /send_2fa` - Resend 2FA code
- `GET /logout` - User logout

### User Management
- `GET /dashboard` - User dashboard
- `POST /change_password` - Password change
- `GET /admin/users` - Admin user management
- `POST /create_user` - Create new user (admin only)
- `POST /delete_user` - Delete user (admin only)

### File Operations
- `GET /editor` - Text editor interface
- `POST /save_file` - Save file content
- `GET /load_file/<filename>` - Load file content
- `POST /delete_file` - Delete user file

### API
- `GET /api/user/<username>` - User information

## ⚙️ Configuration

### Email Setup
Update `email_sender.py` with your Gmail credentials:
1. Enable 2-Step Verification in Google Account
2. Generate App Password for Mail
3. Update encrypted credentials in the file

### Security Settings
Modify `SecurityConfig` in `secure_auth_complete.py`:
- `PASSWORD_MIN_LENGTH` - Minimum password length
- `MAX_LOGIN_ATTEMPTS` - Failed attempts before lockout
- `LOCKOUT_DURATION` - Account lockout time (seconds)
- `SESSION_TIMEOUT` - Session expiry time (seconds)

## 🛡️ Security Best Practices

- ✅ Never expose credentials in logs or APIs
- ✅ Use strong, unique passwords and PINs
- ✅ Enable 2FA for all users
- ✅ Regularly review audit logs
- ✅ Keep email credentials secure
- ✅ Monitor failed login attempts

## 📊 Admin Features

- **User Creation** with email, password, and PIN
- **User Deletion** with file cleanup
- **System Statistics** dashboard
- **Security Monitoring** through audit logs
- **Role Management** for access control

---

**© 2024 Python Authentication System - Enterprise Security Made Simple**